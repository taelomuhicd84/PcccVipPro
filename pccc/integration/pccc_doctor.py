#!/usr/bin/env python3
"""pccc_doctor.py — Kiểm tra sức khỏe module PCCC (chạy trước commit, sau hợp nhất, trong CI).

Dùng:
  python3 pccc/integration/pccc_doctor.py            # kiểm tra nhanh
  python3 pccc/integration/pccc_doctor.py --tests    # kèm chạy unittest pccc/tests
  python3 pccc/integration/pccc_doctor.py --root DIR # kiểm tra repo khác đã cài module

Mã thoát: 0 = không lỗi (có thể có cảnh báo), 1 = có lỗi ✗.
"""
from __future__ import annotations

import argparse
import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pccc_merge as PM  # noqa: E402

CONG_CU_HOP_LE = {"Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Bash", "WebFetch", "WebSearch",
                  "NotebookEdit", "NotebookRead", "TodoWrite", "Task", "Agent", "Skill", "LS"}
NHAN = ("BG", "TC", "DC", "QT")


class KetQua:
    def __init__(self) -> None:
        self.loi: List[str] = []
        self.canh_bao: List[str] = []
        self.ok: List[str] = []

    def them(self, muc: str, dat: bool, chi_tiet: str = "", nhe: bool = False) -> None:
        if dat:
            self.ok.append(muc)
        elif nhe:
            self.canh_bao.append(f"{muc}: {chi_tiet}")
        else:
            self.loi.append(f"{muc}: {chi_tiet}")


def frontmatter(text: str) -> Dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    kq: Dict[str, str] = {"_co": "1"}
    for d in m.group(1).split("\n"):
        mm = re.match(r"^([A-Za-z_-]+):\s*(.*)$", d)
        if mm:
            kq[mm.group(1)] = mm.group(2).strip().strip("'\"")
    return kq


def kiem_tra(root: Path, chay_test: bool) -> KetQua:
    kq = KetQua()
    # 1) manifest / version / config
    try:
        mf = PM.doc_manifest(root)
    except Exception as ex:
        kq.them("manifest.json", False, str(ex))
        return kq
    ver_file = root / "pccc" / "VERSION"
    ver = ver_file.read_text(encoding="utf-8").strip() if ver_file.exists() else None
    kq.them("VERSION khớp manifest", ver == mf["version"], f"VERSION={ver} ≠ manifest={mf['version']}")
    try:
        json.loads((root / "pccc" / "config.json").read_text(encoding="utf-8"))
        kq.them("config.json hợp lệ", True)
    except Exception as ex:
        kq.them("config.json hợp lệ", False, str(ex))

    owned = PM.liet_ke_owned(root, mf)
    kq.them("có file owned", len(owned) > 0, "không tìm thấy file nào của module")

    # 2) JSON & Python & shell
    for rel in owned:
        f = PM.p(root, rel)
        if rel.endswith(".json"):
            try:
                json.loads(f.read_text(encoding="utf-8-sig"))
            except Exception as ex:
                kq.them(f"JSON {rel}", False, str(ex))
        elif rel.endswith(".py"):
            try:
                with tempfile.TemporaryDirectory() as td:
                    py_compile.compile(str(f), cfile=str(Path(td) / "x.pyc"), doraise=True)
            except py_compile.PyCompileError as ex:
                kq.them(f"Python {rel}", False, ex.msg)
        elif rel.endswith(".sh"):
            kq.them(f"LF {rel}", b"\r\n" not in f.read_bytes(), "có CRLF — bash sẽ lỗi")
    kq.ok.append("JSON/Python/shell của module")

    # 3) skills & agents
    ten_skill: Dict[str, str] = {}
    skills_dir = root / ".claude" / "skills"
    if skills_dir.is_dir():
        for d in sorted(skills_dir.iterdir()):
            if not d.is_dir():
                continue
            sk = d / "SKILL.md"
            if d.name.startswith(mf["namespace"]["skill_prefix"]):
                if not sk.exists():
                    kq.them(f"skill {d.name}", False, "thiếu SKILL.md")
                    continue
                fm = frontmatter(sk.read_text(encoding="utf-8"))
                if not fm:
                    kq.them(f"skill {d.name}", False, "thiếu frontmatter")
                    continue
                if fm.get("name") != d.name:
                    kq.them(f"skill {d.name}", False, f"name='{fm.get('name')}' ≠ tên thư mục")
                if not fm.get("description") or len(fm.get("description", "")) > 1024:
                    kq.them(f"skill {d.name}", False, "description rỗng hoặc > 1024 ký tự")
            elif sk.exists():
                t = sk.read_text(encoding="utf-8", errors="replace")[:4000].lower()
                if "pccc" in t or "phòng cháy" in t:
                    kq.them(f"skill {d.name}", False, "có nội dung PCCC nhưng thiếu tiền tố pccc-", nhe=True)
            if sk.exists():
                n = frontmatter(sk.read_text(encoding="utf-8", errors="replace")).get("name") or d.name
                if n in ten_skill:
                    kq.them("tên skill duy nhất", False, f"'{n}' trùng giữa {ten_skill[n]} và {d.name}")
                ten_skill[n] = d.name
    so_skill = sum(1 for n in ten_skill if n.startswith(mf["namespace"]["skill_prefix"]))
    kq.ok.append(f"{so_skill} skill PCCC")
    ten_agent: Dict[str, str] = {}
    agents_dir = root / ".claude" / "agents"
    if agents_dir.is_dir():
        for f in sorted(agents_dir.glob("*.md")):
            fm = frontmatter(f.read_text(encoding="utf-8", errors="replace"))
            n = fm.get("name") or f.stem
            if n in ten_agent:
                kq.them("tên agent duy nhất", False, f"'{n}' trùng giữa {ten_agent[n]} và {f.name}")
            ten_agent[n] = f.name
            if not f.stem.startswith(mf["namespace"]["agent_prefix"]):
                continue
            if not fm:
                kq.them(f"agent {f.stem}", False, "thiếu frontmatter")
                continue
            if fm.get("name") != f.stem:
                kq.them(f"agent {f.stem}", False, f"name='{fm.get('name')}' ≠ tên file")
            if not fm.get("description"):
                kq.them(f"agent {f.stem}", False, "thiếu description")
            if fm.get("tools"):
                la = [t.strip() for t in fm["tools"].split(",") if t.strip()]
                sai = [t for t in la if t not in CONG_CU_HOP_LE and not t.startswith("mcp__")]
                kq.them(f"agent {f.stem} tools", not sai, f"công cụ lạ {sai}", nhe=True)
    kq.ok.append(f"{sum(1 for n in ten_agent if n.startswith(mf['namespace']['agent_prefix']))} agent PCCC")

    # 4) tích hợp file dùng chung + hook
    for f, tt in PM.kiem_tra_shared(root, mf):
        kq.them(f"tích hợp {f}", tt == "ok", tt)
    frag = json.loads(PM.p(root, "pccc/integration/settings.fragment.json").read_text(encoding="utf-8"))
    for ev, nhom in frag.get("hooks", {}).items():
        for g in nhom:
            for h in g.get("hooks", []):
                m = re.search(r"hooks/pccc/run_hook\.sh\"?\s+(\w+)", h.get("command", ""))
                if m:
                    kq.them(f"hook {ev}:{m.group(1)}", (root / ".claude/hooks/pccc" / f"{m.group(1)}.py").exists(),
                            "thiếu script")
    moi = PM._tim_pccc_new(root)
    kq.them("không còn xung đột *.pccc-new", not moi, f"{[x.relative_to(root).as_posix() for x in moi]}")

    # 5) tham chiếu đường dẫn trong tài liệu
    gay = []
    for rel in owned:
        if not rel.endswith(".md"):
            continue
        text = PM.p(root, rel).read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"`((?:pccc|\.claude)/[^`\s]+)`", text):
            ref = m.group(1).rstrip(".,;:)")
            if any(c in ref for c in "<>{}…|") or "..." in ref or PM.bi_loai_tru(ref, mf):
                continue
            if "*" in ref:
                if not list(root.glob(ref)):
                    gay.append(f"{rel} → {ref}")
            elif not PM.p(root, ref.rstrip("/")).exists():
                gay.append(f"{rel} → {ref}")
    kq.them("tham chiếu đường dẫn trong tài liệu", not gay, "; ".join(sorted(set(gay))[:15]))

    # 6) kho tri thức
    kdir = root / "pccc" / "knowledge"
    dem = {n: 0 for n in NHAN}
    if kdir.is_dir():
        for f in sorted(kdir.glob("*.md")):
            t = f.read_text(encoding="utf-8")
            for n in NHAN:
                dem[n] += t.count(f"[{n}]")
            if f.name != "00-muc-luc.md":
                kq.them(f"tri thức {f.name} có dòng 'Cập nhật:'", "Cập nhật:" in t, "thiếu ngày cập nhật", nhe=True)
    kq.ok.append("nhãn tri thức: " + ", ".join(f"[{n}]={dem[n]}" for n in NHAN))
    if dem["DC"]:
        kq.canh_bao.append(f"còn {dem['DC']} số liệu [DC] cần đối chiếu bản gốc (dùng /pccc-cap-nhat-tri-thuc khi có văn bản)")

    # 7) HTML sơ đồ
    html = root / "pccc" / "so_do_note.html"
    if html.exists():
        t = html.read_text(encoding="utf-8")
        kq.them("so_do_note.html có <title>", "<title>" in t, "thiếu <title>")
        kq.them("so_do_note.html cân bằng <svg>", t.count("<svg") == t.count("</svg>"), "thẻ svg không cân bằng")
        ngoai = re.findall(r"<(?:script|link)[^>]+(?:src|href)=\"https?://", t)
        kq.them("so_do_note.html chạy offline", not ngoai, "có tài nguyên ngoài", nhe=True)
    else:
        kq.them("so_do_note.html", False, "thiếu file")

    # 8) unittest
    if chay_test:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(root / "pccc" / "tests")],
                           capture_output=True, text=True, cwd=str(root))
        dong = (r.stderr or r.stdout).strip().splitlines()
        kq.them("unittest pccc/tests", r.returncode == 0, "\n".join(dong[-15:]))
    return kq


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(PM.MODULE_ROOT))
    ap.add_argument("--tests", action="store_true", help="chạy thêm unittest")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    kq = kiem_tra(root, a.tests)
    print(f"PCCC doctor — {root}")
    for x in kq.ok:
        print(f"  ✓ {x}")
    for x in kq.canh_bao:
        print(f"  ⚠ {x}")
    for x in kq.loi:
        print(f"  ✗ {x}")
    print(f"Kết quả: {len(kq.loi)} lỗi, {len(kq.canh_bao)} cảnh báo")
    return 1 if kq.loi else 0


if __name__ == "__main__":
    sys.exit(main())
