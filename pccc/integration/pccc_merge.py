#!/usr/bin/env python3
"""pccc_merge.py — Cài đặt / đồng bộ / gỡ module PCCC vào bất kỳ repo nào (idempotent, an toàn hợp nhất).

Lệnh:
  status    [--target DIR]                      Trạng thái tích hợp tại DIR (mặc định: repo chứa script này)
  check     [--target DIR]                      Như status nhưng trả mã 1 nếu lệch (dùng cho CI / doctor)
  plan      --target DIR                        Phân tích va chạm TRƯỚC khi hợp nhất (không ghi gì)
  install   --target DIR [--dry-run] [--force]  Sao chép/nâng cấp module + chèn khối + gộp settings
  sync      [--target DIR] [--dry-run]          Áp lại khối quản lý & settings (chạy sau git merge/pull)
  resolve   --target DIR FILE...                Đánh dấu đã tự gộp xung đột (xóa *.pccc-new, cập nhật lock)
  uninstall --target DIR [--dry-run] [--force]  Gỡ module khỏi DIR

Nguyên tắc (xem pccc/integration/HOP_NHAT.md):
  • File 'owned' (pccc/, .claude/skills/pccc-*, .claude/agents/pccc-*, .claude/hooks/pccc/) thuộc trọn module.
  • File 'shared' (CLAUDE.md, STRUCTURE.md, MEMORY.md, README.md, .gitignore, .gitattributes, .claude/settings.json)
    thuộc dự án chủ; module chỉ quản lý khối có đánh dấu hoặc mục JSON do nó thêm → không bao giờ ghi đè nội dung khác.
  • Nâng cấp dùng logic 3 chiều (base trong install-lock.json): không mất sửa đổi cục bộ.
Chỉ dùng thư viện chuẩn Python >= 3.8.
"""
from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MODULE_ROOT = Path(__file__).resolve().parents[2]
REL_MANIFEST = "pccc/integration/manifest.json"
REL_LOCK = "pccc/integration/install-lock.json"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass


class LoiKhoi(Exception):
    """Khối đánh dấu bị hỏng (thiếu begin/end, lồng nhau...)."""


# =============================================================================== tiện ích
def doc_manifest(root: Path = MODULE_ROOT) -> Dict[str, Any]:
    return json.loads((root / REL_MANIFEST).read_text(encoding="utf-8"))


def p(root: Path, rel: str) -> Path:
    return root.joinpath(*rel.split("/"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class TepVanBan:
    """Đọc/ghi văn bản giữ nguyên BOM và kiểu xuống dòng (LF/CRLF) của file đích."""

    def __init__(self, path: Path):
        self.path = path
        raw = path.read_bytes() if path.exists() else None
        self.ton_tai = raw is not None
        self.bom = bool(raw) and raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig") if raw else ""
        self.eol = "\r\n" if "\r\n" in text else "\n"
        self.text = text.replace("\r\n", "\n")

    def ghi(self, text: str) -> None:
        b = text.replace("\n", self.eol).encode("utf-8")
        if self.bom:
            b = b"\xef\xbb\xbf" + b
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_bytes(b)


def khop_mau(rel: str, mau: str) -> bool:
    rp = rel.split("/")
    if mau.endswith("/"):
        pp = mau.rstrip("/").split("/")
        return len(rp) > len(pp) and all(fnmatch.fnmatchcase(rp[i], pp[i]) for i in range(len(pp)))
    pp = mau.split("/")
    return len(rp) == len(pp) and all(fnmatch.fnmatchcase(rp[i], pp[i]) for i in range(len(pp)))


def bi_loai_tru(rel: str, mf: Dict[str, Any]) -> bool:
    phan = rel.split("/")
    for mau in mf.get("exclude", []):
        if mau.startswith("**/"):
            con = mau[3:]
            if con.endswith("/**"):
                if con[:-3] in phan[:-1]:
                    return True
            elif fnmatch.fnmatchcase(phan[-1], con):
                return True
        elif fnmatch.fnmatchcase(rel, mau):
            return True
    return False


def la_owned(rel: str, mf: Dict[str, Any]) -> bool:
    return any(khop_mau(rel, m) for m in mf["owned"]) and not bi_loai_tru(rel, mf)


def la_union(rel: str, mf: Dict[str, Any]) -> bool:
    return any(khop_mau(rel, m) for m in mf.get("merge_union", []))


def liet_ke_owned(root: Path, mf: Dict[str, Any]) -> List[str]:
    kq = set()
    for mau in mf["owned"]:
        tinh = []
        for phan in mau.rstrip("/").split("/"):
            if any(c in phan for c in "*?["):
                break
            tinh.append(phan)
        goc = p(root, "/".join(tinh)) if tinh else root
        if goc.is_file():
            rel = goc.relative_to(root).as_posix()
            if la_owned(rel, mf):
                kq.add(rel)
            continue
        if not goc.is_dir():
            continue
        for dp, dn, fn in os.walk(goc):
            dn[:] = [d for d in dn if d not in ("__pycache__", ".pytest_cache", ".git")]
            for f in fn:
                rel = (Path(dp) / f).relative_to(root).as_posix()
                if la_owned(rel, mf):
                    kq.add(rel)
    return sorted(kq)


def doc_lock(root: Path) -> Optional[Dict[str, Any]]:
    f = p(root, REL_LOCK)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return None


# =============================================================================== khối đánh dấu
def _mau_khoi(kieu: str, module: str) -> Tuple["re.Pattern[str]", "re.Pattern[str]"]:
    m = re.escape(module)
    if kieu == "md-block":
        return (re.compile(rf"^\s*<!--\s*{m}:begin\b.*-->\s*$"), re.compile(rf"^\s*<!--\s*{m}:end\b.*-->\s*$"))
    return (re.compile(rf"^\s*#\s*{m}:begin\b.*$"), re.compile(rf"^\s*#\s*{m}:end\b.*$"))


def dong_danh_dau(kieu: str, mf: Dict[str, Any]) -> Tuple[str, str]:
    mod, ver = mf["module"], mf["version"]
    if kieu == "md-block":
        return (f"<!-- {mod}:begin · module {mod} v{ver} · quản lý bởi pccc/integration/pccc_merge.py — "
                f"sửa ở pccc/integration/blocks/, đừng sửa tay trong khối -->", f"<!-- {mod}:end -->")
    return (f"# {mod}:begin · module {mod} v{ver} · quản lý bởi pccc/integration/pccc_merge.py", f"# {mod}:end")


def tim_khoi(dong: List[str], kieu: str, module: str) -> Optional[Tuple[int, int]]:
    rb, re_ = _mau_khoi(kieu, module)
    bd = [i for i, d in enumerate(dong) if rb.match(d)]
    kt = [i for i, d in enumerate(dong) if re_.match(d)]
    if not bd and not kt:
        return None
    if len(bd) != 1 or len(kt) != 1 or kt[0] < bd[0]:
        raise LoiKhoi(f"khối '{module}' hỏng: {len(bd)} dòng begin, {len(kt)} dòng end")
    return bd[0], kt[0]


def _tach_dong(text: str) -> List[str]:
    if not text:
        return []
    dong = text.split("\n")
    if text.endswith("\n"):
        dong = dong[:-1]
    return dong


def ap_khoi(text: str, kieu: str, noi_dung: str, mf: Dict[str, Any], tieu_de: Optional[str] = None) -> str:
    dong = _tach_dong(text)
    b, e = dong_danh_dau(kieu, mf)
    khoi = [b] + noi_dung.strip("\n").split("\n") + [e]
    vt = tim_khoi(dong, kieu, mf["module"])
    if vt:
        dong[vt[0]:vt[1] + 1] = khoi
    else:
        if not any(x.strip() for x in dong):
            dong = tieu_de.split("\n") if tieu_de else []
        if dong and dong[-1].strip():
            dong.append("")
        dong.extend(khoi)
    return "\n".join(dong) + "\n"


def go_khoi(text: str, kieu: str, module: str) -> str:
    dong = _tach_dong(text)
    vt = tim_khoi(dong, kieu, module)
    if not vt:
        return text
    s, e = vt
    del dong[s:e + 1]
    if s > 0 and not dong[s - 1].strip() and (s >= len(dong) or not dong[s].strip()):
        del dong[s - 1]
    return ("\n".join(dong) + "\n") if dong else ""


def noi_dung_khoi(text: str, kieu: str, module: str) -> Optional[str]:
    dong = _tach_dong(text)
    vt = tim_khoi(dong, kieu, module)
    if not vt:
        return None
    return "\n".join(dong[vt[0]:vt[1] + 1])


# =============================================================================== settings.json
def _do_thut_json(text: str) -> int:
    for d in text.split("\n")[1:]:
        m = re.match(r"^( +)\S", d)
        if m:
            return len(m.group(1))
    return 2


def go_settings(cfg: Dict[str, Any], marker: str, quyen_da_them: Optional[Dict[str, List[str]]] = None,
                khoa_da_them: Optional[List[str]] = None) -> Dict[str, Any]:
    out = copy.deepcopy(cfg)
    hooks = out.get("hooks")
    if isinstance(hooks, dict):
        for ev in list(hooks):
            nhom = hooks[ev]
            if not isinstance(nhom, list):
                continue
            moi = []
            for g in nhom:
                hs = g.get("hooks", []) if isinstance(g, dict) else []
                giu = [h for h in hs if marker not in str(h.get("command", ""))]
                if hs and not giu:
                    continue  # nhóm chỉ chứa hook của module → bỏ cả nhóm
                if len(giu) != len(hs):
                    g = dict(g)
                    g["hooks"] = giu
                moi.append(g)
            if moi:
                hooks[ev] = moi
            elif nhom:
                del hooks[ev]
        if not hooks and "hooks" in cfg and cfg["hooks"]:
            del out["hooks"]
    if quyen_da_them:
        perm = out.get("permissions", {})
        for k, ds in quyen_da_them.items():
            if isinstance(perm.get(k), list):
                perm[k] = [x for x in perm[k] if x not in ds]
                if not perm[k]:
                    del perm[k]
        if "permissions" in out and not out["permissions"]:
            del out["permissions"]
    for k in khoa_da_them or []:
        out.pop(k, None)
    return out


def gop_settings(cfg: Dict[str, Any], frag: Dict[str, Any], marker: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Gộp fragment vào settings: bỏ hook cũ của module rồi thêm bản mới; hợp quyền; thêm khóa thiếu."""
    out = go_settings(cfg, marker)
    da_them: Dict[str, Any] = {"permissions": {}, "top_level": []}
    for k, v in frag.items():
        if k in ("hooks", "permissions"):
            continue
        if k not in out:
            out[k] = copy.deepcopy(v)
            da_them["top_level"].append(k)
    for k, ds in frag.get("permissions", {}).items():
        perm = out.setdefault("permissions", {})
        hien = perm.setdefault(k, [])
        for x in ds:
            if x not in hien:
                hien.append(x)
                da_them["permissions"].setdefault(k, []).append(x)
    for ev, nhom in frag.get("hooks", {}).items():
        dich = out.setdefault("hooks", {}).setdefault(ev, [])
        for g in nhom:
            m = g.get("matcher", "")
            tg = next((x for x in dich if isinstance(x, dict) and x.get("matcher", "") == m), None)
            if tg is None:
                dich.append(copy.deepcopy(g))
            else:
                tg.setdefault("hooks", []).extend(copy.deepcopy(g.get("hooks", [])))
    return out, da_them


# =============================================================================== áp dụng file dùng chung
def ap_dung_shared(dich: Path, goc_module: Path, mf: Dict[str, Any], dry: bool,
                   lock_cu: Optional[Dict[str, Any]] = None) -> Tuple[List[str], Dict[str, Any], List[str]]:
    """Chèn/cập nhật khối & gộp settings. Trả (thay đổi, thông tin lock 'shared', lỗi)."""
    thay_doi: List[str] = []
    loi: List[str] = []
    info: Dict[str, Any] = copy.deepcopy((lock_cu or {}).get("shared", {}))
    marker = mf["hook_command_marker"]
    for sh in mf["shared"]:
        f = p(dich, sh["path"])
        nguon = p(goc_module, sh["source"])
        tf = TepVanBan(f)
        rec = info.setdefault(sh["path"], {})
        if not tf.ton_tai:
            rec["tao_moi"] = True
        if sh["type"] in ("md-block", "hash-block"):
            nd = nguon.read_text(encoding="utf-8")
            try:
                moi = ap_khoi(tf.text, sh["type"], nd, mf, sh.get("tieu_de_khi_tao"))
            except LoiKhoi as ex:
                loi.append(f"{sh['path']}: {ex} — sửa tay cho còn đúng 1 cặp begin/end rồi chạy lại")
                continue
            if moi != tf.text:
                thay_doi.append(f"{'tạo' if not tf.ton_tai else 'cập nhật khối'} {sh['path']}")
                if not dry:
                    tf.ghi(moi)
        elif sh["type"] == "json-merge":
            frag = json.loads(nguon.read_text(encoding="utf-8"))
            try:
                cfg = json.loads(tf.text) if tf.text.strip() else {}
            except json.JSONDecodeError as ex:
                loi.append(f"{sh['path']}: JSON không hợp lệ ({ex}) — sửa file rồi chạy lại; KHÔNG ghi đè")
                continue
            moi, da_them = gop_settings(cfg, frag, marker)
            for k, ds in da_them["permissions"].items():
                cu = rec.setdefault("permissions", {}).setdefault(k, [])
                cu.extend(x for x in ds if x not in cu)
            rec.setdefault("top_level", [])
            rec["top_level"].extend(x for x in da_them["top_level"] if x not in rec["top_level"])
            if moi != cfg:
                thay_doi.append(f"{'tạo' if not tf.ton_tai else 'gộp'} {sh['path']}")
                if not dry:
                    tf.ghi(json.dumps(moi, ensure_ascii=False, indent=_do_thut_json(tf.text)) + "\n")
    return thay_doi, info, loi


def kiem_tra_shared(dich: Path, mf: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Trả danh sách (file, trạng thái) — trạng thái 'ok' | mô tả lệch."""
    kq = []
    marker = mf["hook_command_marker"]
    for sh in mf["shared"]:
        f = p(dich, sh["path"])
        nguon = p(dich, sh["source"])
        if not nguon.exists():
            kq.append((sh["path"], f"thiếu nguồn {sh['source']}"))
            continue
        tf = TepVanBan(f)
        if not tf.ton_tai:
            kq.append((sh["path"], "chưa có file"))
            continue
        if sh["type"] in ("md-block", "hash-block"):
            try:
                moi = ap_khoi(tf.text, sh["type"], nguon.read_text(encoding="utf-8"), mf, sh.get("tieu_de_khi_tao"))
            except LoiKhoi as ex:
                kq.append((sh["path"], f"khối hỏng: {ex}"))
                continue
            kq.append((sh["path"], "ok" if moi == tf.text else "khối lệch nguồn → chạy sync"))
        else:
            try:
                cfg = json.loads(tf.text) if tf.text.strip() else {}
            except json.JSONDecodeError as ex:
                kq.append((sh["path"], f"JSON lỗi: {ex}"))
                continue
            moi, _ = gop_settings(cfg, json.loads(nguon.read_text(encoding="utf-8")), marker)
            kq.append((sh["path"], "ok" if moi == cfg else "thiếu/lệch hook hoặc quyền của module → chạy sync"))
    return kq


# =============================================================================== lập kế hoạch file owned
def lap_ke_hoach(src: Path, dich: Path, mf: Dict[str, Any], force: bool) -> List[Tuple[str, str]]:
    lock = doc_lock(dich) or {}
    base_map: Dict[str, str] = lock.get("files", {})
    ds_src = liet_ke_owned(src, mf)
    tap_src = set(ds_src)
    kh: List[Tuple[str, str]] = []
    for rel in ds_src:
        t = p(dich, rel)
        if not t.exists():
            kh.append(("copy", rel))
            continue
        hs, ht = sha256(p(src, rel)), sha256(t)
        base = base_map.get(rel)
        if hs == ht:
            kh.append(("same", rel))
        elif base and ht == base:
            kh.append(("update", rel))
        elif base and hs == base:
            kh.append(("keep-local", rel))
        elif la_union(rel, mf):
            kh.append(("union", rel))
        elif force:
            kh.append(("overwrite", rel))
        else:
            kh.append(("conflict", rel))
    for rel, base in base_map.items():
        if rel in tap_src:
            continue
        t = p(dich, rel)
        if t.exists():
            kh.append(("delete" if sha256(t) == base else "orphan", rel))
    return kh


def _gop_union(dich_txt: str, src_txt: str) -> str:
    co = set(dich_txt.split("\n"))
    them = [d for d in src_txt.split("\n") if d not in co and d.strip()]
    if not them:
        return dich_txt
    return dich_txt.rstrip("\n") + "\n" + "\n".join(them) + "\n"


# =============================================================================== lệnh
def lenh_install(dich: Path, dry: bool, force: bool) -> int:
    src = MODULE_ROOT
    if dich.resolve() == src.resolve():
        print("⛔ Đích trùng repo nguồn — dùng 'sync' để áp lại tích hợp tại chỗ.")
        return 1
    if not dich.is_dir():
        print(f"⛔ Không thấy thư mục đích: {dich}")
        return 1
    mf = doc_manifest(src)
    lock_cu = doc_lock(dich) or {}
    kh = lap_ke_hoach(src, dich, mf, force)
    dem: Dict[str, int] = {}
    files_lock: Dict[str, str] = dict(lock_cu.get("files", {}))
    xung_dot, mo_coi = [], []
    for hd, rel in kh:
        dem[hd] = dem.get(hd, 0) + 1
        s, t = p(src, rel), p(dich, rel)
        if hd in ("copy", "update", "overwrite"):
            if not dry:
                t.parent.mkdir(parents=True, exist_ok=True)
                if hd == "overwrite":
                    shutil.copy2(t, t.with_name(t.name + ".pccc-bak"))
                shutil.copy2(s, t)
            files_lock[rel] = sha256(s)
        elif hd == "same":
            files_lock[rel] = sha256(s)
        elif hd == "union":
            if not dry:
                tf = TepVanBan(t)
                tf.ghi(_gop_union(tf.text, s.read_text(encoding="utf-8")))
            files_lock[rel] = sha256(s)
        elif hd == "conflict":
            xung_dot.append(rel)
            if not dry:
                shutil.copy2(s, t.with_name(t.name + ".pccc-new"))
        elif hd == "delete":
            if not dry:
                t.unlink()
            files_lock.pop(rel, None)
        elif hd == "orphan":
            mo_coi.append(rel)
            files_lock.pop(rel, None)
    if not dry and dem.get("delete"):
        _don_thu_muc_rong(dich, mf)
    # tích hợp file dùng chung — đọc nguồn khối từ đích (đã cập nhật) hoặc từ nguồn khi dry-run
    thay, info_shared, loi = ap_dung_shared(dich, src if dry else dich, mf, dry, lock_cu)
    print(f"{'[DRY-RUN] ' if dry else ''}Cài module {mf['module']} v{mf['version']} → {dich}")
    for k in ("copy", "update", "same", "keep-local", "union", "overwrite", "conflict", "delete", "orphan"):
        if dem.get(k):
            print(f"  {k:<11} {dem[k]}")
    for x in thay:
        print(f"  • {x}")
    for rel in xung_dot:
        print(f"  ⚠ XUNG ĐỘT {rel} → bản mới ở {rel}.pccc-new; tự gộp rồi chạy: "
              f"python3 pccc/integration/pccc_merge.py resolve --target . {rel}")
    for rel in mo_coi:
        print(f"  ⚠ {rel} không còn trong module nhưng đã bị sửa ở đích → giữ nguyên, tự quyết định xóa")
    for x in loi:
        print(f"  ⛔ {x}")
    if not dry:
        lock = {"module": mf["module"], "version": mf["version"],
                "cai_luc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "nguon": str(src), "files": dict(sorted(files_lock.items())), "shared": info_shared}
        lf = p(dich, REL_LOCK)
        lf.parent.mkdir(parents=True, exist_ok=True)
        lf.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  lock: {REL_LOCK}")
    print("Tiếp theo: cd <đích> && python3 pccc/integration/pccc_doctor.py")
    return 1 if (loi or xung_dot) else 0


def lenh_sync(dich: Path, dry: bool) -> int:
    if not p(dich, REL_MANIFEST).exists():
        print(f"⛔ {dich} chưa có module (thiếu {REL_MANIFEST}). Dùng install.")
        return 1
    mf = doc_manifest(dich)
    lock = doc_lock(dich)
    thay, info, loi = ap_dung_shared(dich, dich, mf, dry, lock)
    print(f"{'[DRY-RUN] ' if dry else ''}Đồng bộ tích hợp module {mf['module']} v{mf['version']} tại {dich}")
    for x in thay:
        print(f"  • {x}")
    if not thay and not loi:
        print("  ✓ Không có gì thay đổi (đã đồng bộ)")
    for x in loi:
        print(f"  ⛔ {x}")
    if lock is not None and not dry:
        lock["shared"] = info
        p(dich, REL_LOCK).write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if loi else 0


def lenh_status(dich: Path, nghiem: bool) -> int:
    if not p(dich, REL_MANIFEST).exists():
        print(f"Module PCCC chưa có trong {dich}")
        return 1
    mf = doc_manifest(dich)
    lock = doc_lock(dich)
    ds = liet_ke_owned(dich, mf)
    print(f"Module {mf['module']} v{mf['version']} tại {dich}")
    print(f"  File owned: {len(ds)}; lock: {'có (cài từ ' + lock.get('nguon', '?') + ')' if lock else 'không (repo nguồn)'}")
    lech = 0
    for f, tt in kiem_tra_shared(dich, mf):
        dau = "✓" if tt == "ok" else "✗"
        lech += tt != "ok"
        print(f"  {dau} {f}: {tt}")
    if lock:
        sua = [rel for rel, h in lock.get("files", {}).items() if p(dich, rel).exists() and sha256(p(dich, rel)) != h]
        if sua:
            print(f"  ℹ {len(sua)} file module đã sửa cục bộ so với bản cài (sẽ được giữ khi nâng cấp)")
        moi = [x.relative_to(dich).as_posix() for x in _tim_pccc_new(dich)]
        if moi:
            lech += len(moi)
            print(f"  ✗ Còn {len(moi)} xung đột chưa giải quyết: {moi[:5]}")
    return 1 if (nghiem and lech) else 0


def _doc_frontmatter_name(f: Path) -> Optional[str]:
    try:
        t = f.read_text(encoding="utf-8")
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", t, re.S)
    if not m:
        return None
    n = re.search(r"^name:\s*(.+?)\s*$", m.group(1), re.M)
    return n.group(1).strip("'\"") if n else None


def lenh_plan(dich: Path) -> int:
    src = MODULE_ROOT
    mf = doc_manifest(src)
    if not dich.is_dir():
        print(f"⛔ Không thấy thư mục đích: {dich}")
        return 1
    chan = 0
    print(f"# Kế hoạch hợp nhất module {mf['module']} v{mf['version']} → {dich}\n")
    print(f"- Git repo: {'có' if (dich / '.git').exists() else 'KHÔNG (khuyên: git init + commit trước để dễ hoàn tác)'}")
    kh = lap_ke_hoach(src, dich, mf, False)
    dem: Dict[str, int] = {}
    for hd, _ in kh:
        dem[hd] = dem.get(hd, 0) + 1
    print("- File của module: " + ", ".join(f"{k}={v}" for k, v in sorted(dem.items())))
    for hd, rel in kh:
        if hd in ("conflict", "orphan"):
            print(f"  - ⚠ {hd}: {rel}")
    print("\n## File dùng chung")
    for sh in mf["shared"]:
        f = p(dich, sh["path"])
        if not f.exists():
            print(f"- {sh['path']}: chưa có → sẽ tạo mới")
            continue
        tf = TepVanBan(f)
        if sh["type"] == "json-merge":
            try:
                cfg = json.loads(tf.text) if tf.text.strip() else {}
                n_hook = sum(len(g.get("hooks", [])) for ds in cfg.get("hooks", {}).values() for g in ds
                             if isinstance(g, dict))
                print(f"- {sh['path']}: JSON hợp lệ, {n_hook} hook sẵn có → sẽ GỘP (không xóa gì)")
                for ev, ds in cfg.get("hooks", {}).items():
                    for g in ds:
                        for h in g.get("hooks", []):
                            cmd = str(h.get("command", ""))
                            if mf["hook_command_marker"] in cmd:
                                continue
                            if ev in ("PreToolUse", "PostToolUse") and re.search(r"Write|Edit|\*", str(g.get("matcher", "*"))):
                                print(f"  - ℹ hook {ev}[{g.get('matcher', '*')}] của dự án đích có thể chặn/sửa thao tác ghi file: {cmd[:90]}")
                for rule in cfg.get("permissions", {}).get("deny", []):
                    if re.search(r"python|pccc|Bash\(\*\)|^Bash$", rule):
                        print(f"  - ⚠ quyền deny '{rule}' có thể chặn công cụ PCCC")
            except json.JSONDecodeError as ex:
                chan += 1
                print(f"- ⛔ {sh['path']}: JSON lỗi ({ex}) — phải sửa trước khi hợp nhất")
            continue
        try:
            vt = tim_khoi(_tach_dong(tf.text), sh["type"], mf["module"])
            khac = sorted(set(re.findall(r"<!--\s*([\w.-]+):begin", tf.text) +
                              re.findall(r"^#\s*([\w.-]+):begin", tf.text, re.M)) - {mf["module"]})
            print(f"- {sh['path']}: {'đã có khối → cập nhật' if vt else 'chưa có khối → nối thêm cuối file'}"
                  f"{'; khối module khác: ' + ', '.join(khac) if khac else ''}"
                  f"{'; CRLF' if tf.eol == chr(13) + chr(10) else ''}{'; BOM' if tf.bom else ''}")
        except LoiKhoi as ex:
            chan += 1
            print(f"- ⛔ {sh['path']}: {ex}")
    print("\n## Va chạm tên tài sản Claude")
    ten_cua_ta = set()
    for rel in liet_ke_owned(src, mf):
        if rel.endswith("SKILL.md") or rel.startswith(".claude/agents/"):
            n = _doc_frontmatter_name(p(src, rel))
            if n:
                ten_cua_ta.add(n)
    va = 0
    for thu_muc in (".claude/skills", ".claude/agents", ".claude/commands"):
        goc = p(dich, thu_muc)
        if not goc.is_dir():
            continue
        for f in goc.rglob("*.md"):
            rel = f.relative_to(dich).as_posix()
            if la_owned(rel, mf):
                continue
            n = _doc_frontmatter_name(f) or f.parent.name if f.name == "SKILL.md" else (_doc_frontmatter_name(f) or f.stem)
            if n in ten_cua_ta or str(n).startswith(mf["namespace"]["skill_prefix"]):
                va += 1
                print(f"- ⚠ {rel}: tên '{n}' trùng/chiếm tiền tố của module")
    if not va:
        print("- Không có va chạm tên skill/agent/command")
    py = shutil.which("python3") or shutil.which("python") or shutil.which("py")
    print(f"\n- Python cho hooks: {py or 'KHÔNG THẤY (hooks sẽ tự bỏ qua — vẫn an toàn)'}")
    print("\n## Lệnh đề xuất")
    print(f"python3 {Path(__file__).resolve()} install --target {dich} --dry-run")
    print(f"python3 {Path(__file__).resolve()} install --target {dich}")
    print("cd <đích> && python3 pccc/integration/pccc_doctor.py && python3 -m unittest discover -s pccc/tests")
    return 1 if chan else 0


def lenh_resolve(dich: Path, ds: List[str]) -> int:
    lock = doc_lock(dich)
    if not lock:
        print("⛔ Không có install-lock.json ở đích")
        return 1
    src = MODULE_ROOT
    for rel in ds:
        rel = rel.replace("\\", "/")
        s = p(src, rel)
        if not s.exists():
            print(f"⛔ {rel} không có trong module nguồn")
            continue
        lock["files"][rel] = sha256(s)
        moi = p(dich, rel + ".pccc-new")
        if moi.exists():
            moi.unlink()
        print(f"✓ Đã đánh dấu gộp xong: {rel}")
    p(dich, REL_LOCK).write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


def _tim_pccc_new(dich: Path) -> List[Path]:
    kq: List[Path] = []
    for goc in ("pccc", ".claude"):
        g = p(dich, goc)
        if g.is_dir():
            kq.extend(g.rglob("*.pccc-new"))
    return kq


def _don_thu_muc_rong(dich: Path, mf: Dict[str, Any]) -> None:
    for goc in ("pccc", ".claude/skills", ".claude/agents", ".claude/hooks/pccc"):
        g = p(dich, goc)
        if not g.is_dir():
            continue
        for dp, dn, fn in sorted(os.walk(g), key=lambda x: -len(x[0])):
            d = Path(dp)
            rel = d.relative_to(dich).as_posix() + "/"
            if not any(d.iterdir()) and (la_owned(rel + "x", mf) or rel.startswith("pccc/")):
                d.rmdir()
    # thư mục cha chung chỉ chứa tài sản module (git không theo dõi thư mục rỗng nên xóa là vô hại)
    for cha in (".claude/hooks", ".claude/skills", ".claude/agents"):
        g = p(dich, cha)
        if g.is_dir() and not any(g.iterdir()):
            g.rmdir()


def lenh_uninstall(dich: Path, dry: bool, force: bool) -> int:
    if dich.resolve() == MODULE_ROOT.resolve():
        print("⛔ Không gỡ module khỏi chính repo nguồn.")
        return 1
    lock = doc_lock(dich)
    if not lock and not force:
        print("⛔ Đích không có install-lock.json (không cài bằng công cụ). Dùng --force để gỡ các file trùng nội dung nguồn.")
        return 1
    mf = doc_manifest(dich) if p(dich, REL_MANIFEST).exists() else doc_manifest(MODULE_ROOT)
    giu = []
    # 1) file dùng chung
    for sh in mf["shared"]:
        f = p(dich, sh["path"])
        if not f.exists():
            continue
        tf = TepVanBan(f)
        rec = (lock or {}).get("shared", {}).get(sh["path"], {})
        if sh["type"] in ("md-block", "hash-block"):
            try:
                moi = go_khoi(tf.text, sh["type"], mf["module"])
            except LoiKhoi as ex:
                print(f"  ⛔ {sh['path']}: {ex}")
                continue
            con = moi.strip()
            xoa = rec.get("tao_moi") and (not con or con == (sh.get("tieu_de_khi_tao") or "").strip())
        else:
            try:
                cfg = json.loads(tf.text) if tf.text.strip() else {}
            except json.JSONDecodeError as ex:
                print(f"  ⛔ {sh['path']}: JSON lỗi ({ex})")
                continue
            q = rec.get("permissions") or (json.loads(p(dich, sh["source"]).read_text(encoding="utf-8")).get("permissions")
                                           if not lock and p(dich, sh["source"]).exists() else {})
            ob = go_settings(cfg, mf["hook_command_marker"], q, rec.get("top_level", []))
            moi = json.dumps(ob, ensure_ascii=False, indent=_do_thut_json(tf.text)) + "\n" if ob != cfg else tf.text
            xoa = rec.get("tao_moi") and not ob
        if xoa:
            print(f"  • xóa {sh['path']} (do module tạo, nay rỗng)")
            if not dry:
                f.unlink()
        elif moi != tf.text:
            print(f"  • gỡ phần module khỏi {sh['path']}")
            if not dry:
                tf.ghi(moi)
    # 2) file owned
    files = (lock or {}).get("files") or {rel: sha256(p(MODULE_ROOT, rel)) for rel in liet_ke_owned(MODULE_ROOT, mf)}
    for rel, base in sorted(files.items()):
        t = p(dich, rel)
        if not t.exists():
            continue
        if sha256(t) == base or (force and lock):
            if not dry:
                t.unlink()
        else:
            giu.append(rel)
    if not dry:
        lf = p(dich, REL_LOCK)
        if lf.exists() and not giu:
            lf.unlink()
        for x in _tim_pccc_new(dich):
            x.unlink()
        _don_thu_muc_rong(dich, mf)
    print(f"{'[DRY-RUN] ' if dry else ''}Gỡ module {mf['module']} khỏi {dich}: xong")
    for rel in giu:
        print(f"  ⚠ giữ lại (đã sửa cục bộ): {rel} — dùng --force để xóa")
    if not dry:
        con = [rel for rel in liet_ke_owned(dich, mf) if rel not in giu]
        for rel in con[:20]:
            print(f"  ℹ giữ lại (không thuộc bản cài — dữ liệu người dùng?): {rel}")
    return 0


# =============================================================================== CLI
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    for ten in ("status", "check", "sync"):
        sp = sub.add_parser(ten)
        sp.add_argument("--target", default=str(MODULE_ROOT))
        if ten == "sync":
            sp.add_argument("--dry-run", action="store_true")
    sp = sub.add_parser("plan")
    sp.add_argument("--target", required=True)
    for ten in ("install", "uninstall"):
        sp = sub.add_parser(ten)
        sp.add_argument("--target", required=True)
        sp.add_argument("--dry-run", action="store_true")
        sp.add_argument("--force", action="store_true")
    sp = sub.add_parser("resolve")
    sp.add_argument("--target", required=True)
    sp.add_argument("files", nargs="+")
    a = ap.parse_args(argv)
    dich = Path(a.target).expanduser().resolve()
    if a.lenh == "status":
        return lenh_status(dich, False)
    if a.lenh == "check":
        return lenh_status(dich, True)
    if a.lenh == "sync":
        return lenh_sync(dich, a.dry_run)
    if a.lenh == "plan":
        return lenh_plan(dich)
    if a.lenh == "install":
        return lenh_install(dich, a.dry_run, a.force)
    if a.lenh == "uninstall":
        return lenh_uninstall(dich, a.dry_run, a.force)
    if a.lenh == "resolve":
        return lenh_resolve(dich, a.files)
    return 1


if __name__ == "__main__":
    sys.exit(main())
