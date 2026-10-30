"""PreToolUse (Write|Edit|MultiEdit): bảo vệ khối do module quản lý & quy ước tiền tố. Fail-open.

R1  Không cho sửa tay nội dung bên trong khối <!-- pccc:begin --> … <!-- pccc:end --> (hoặc # pccc:begin/end)
    của file dùng chung (CLAUDE.md, STRUCTURE.md, MEMORY.md, README.md, .gitignore, .gitattributes):
    phải sửa nguồn ở pccc/integration/blocks/ rồi chạy pccc_merge.py sync. Bỏ qua: PCCC_ALLOW_BLOCK_EDIT=1.
R2  Tài sản Claude mới (skills/agents/commands/hooks) có nội dung PCCC phải mang tiền tố 'pccc-' (chống va chạm
    tên khi hợp nhất). Cấu hình: pccc/config.json → hooks.guard_namespace = block | warn | off.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pccc_hook_common as H  # noqa: E402


def _vung_khoi(text: str, kieu: str, module: str, pm) -> tuple:
    dong = text.split("\n")
    vt = pm.tim_khoi(dong, kieu, module)
    if not vt:
        return ()
    bd = sum(len(d) + 1 for d in dong[:vt[0]])
    kt = sum(len(d) + 1 for d in dong[:vt[1] + 1])
    return (bd, kt)


def kiem_tra_khoi(root: Path, rel: str, tool: str, ti: dict, mf: dict) -> None:
    sh = next((s for s in mf.get("shared", []) if s["path"] == rel and s["type"] in ("md-block", "hash-block")), None)
    if not sh or os.environ.get("PCCC_ALLOW_BLOCK_EDIT") == "1":
        return
    f = root / rel
    if not f.exists():
        return
    pm = H.nap_merge(root)
    if pm is None:
        return
    cur = f.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    try:
        vung = _vung_khoi(cur, sh["type"], mf["module"], pm)
    except Exception:
        return  # khối đang hỏng → để lint/sync báo, không chặn việc sửa chữa
    if not vung:
        return
    ly_do = (f"⛔ [PCCC] Đoạn bạn sửa nằm trong KHỐI do module PCCC quản lý của {rel}. "
             f"Hãy sửa nguồn ở {sh['source']} rồi chạy: python3 pccc/integration/pccc_merge.py sync "
             "(phần ngoài khối thì sửa bình thường; buộc sửa tay: đặt PCCC_ALLOW_BLOCK_EDIT=1).")
    if tool == "Write":
        moi = str(ti.get("content", "")).replace("\r\n", "\n")
        try:
            cu_khoi = pm.noi_dung_khoi(cur, sh["type"], mf["module"])
            moi_khoi = pm.noi_dung_khoi(moi, sh["type"], mf["module"])
        except Exception:
            H.chan(ly_do)
            return
        if cu_khoi != moi_khoi:
            H.chan(ly_do)
        return
    sua = [ti] if tool == "Edit" else list(ti.get("edits", []))
    for e in sua:
        old = str(e.get("old_string", "")).replace("\r\n", "\n")
        if not old:
            continue
        i = cur.find(old)
        while i != -1:
            if i < vung[1] and i + len(old) > vung[0]:
                H.chan(ly_do)
            i = cur.find(old, i + 1)


def kiem_tra_tien_to(root: Path, rel: str, tool: str, ti: dict, cfg: dict) -> None:
    if cfg["hooks"].get("guard_namespace", "block") != "block" or tool != "Write" or (root / rel).exists():
        return
    m = re.match(r"^\.claude/(skills|agents|commands|hooks)/([^/]+)", rel)
    if not m or m.group(2).lower().startswith("pccc"):
        return
    if H.co_dau_hieu_pccc(str(ti.get("content", ""))[:4000]):
        H.chan(f"⛔ [PCCC] Tài sản Claude có nội dung PCCC phải mang tiền tố 'pccc-' để không va chạm khi hợp nhất "
               f"(ví dụ: .claude/{m.group(1)}/pccc-{m.group(2)}). Nếu đây là tài sản của module khác, đặt "
               "hooks.guard_namespace='warn' trong pccc/config.json.")


def main() -> None:
    data = H.doc_input()
    tool = data.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit"):
        return
    ti = data.get("tool_input") or {}
    root = H.thu_muc_du_an(data)
    rel = H.rel_path(root, ti.get("file_path"))
    mf = H.doc_manifest(root)
    if not rel or not mf:
        return
    cfg = H.doc_config(root)
    if cfg["hooks"].get("guard_managed_blocks", True):
        kiem_tra_khoi(root, rel, tool, ti, mf)
    kiem_tra_tien_to(root, rel, tool, ti, cfg)


H.chay_an_toan(main)
