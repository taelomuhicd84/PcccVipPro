"""PostToolUse (Write|Edit|MultiEdit): kiểm tra nhanh file thuộc module PCCC vừa ghi. Fail-open.

Lỗi → exit 2 + mô tả (Claude thấy và tự sửa). Chỉ kiểm tra file của module hoặc file dùng chung có khối PCCC.
"""
from __future__ import annotations

import json
import py_compile
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pccc_hook_common as H  # noqa: E402


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    kq = {}
    for d in m.group(1).split("\n"):
        mm = re.match(r"^([A-Za-z_-]+):\s*(.*)$", d)
        if mm:
            kq[mm.group(1)] = mm.group(2).strip().strip("'\"")
    kq["_co"] = True
    return kq


def kiem_tra(root: Path, rel: str, mf: dict, cfg: dict) -> list:
    loi = []
    f = root / rel
    if not f.exists():
        return loi
    pm = H.nap_merge(root)
    owned = bool(pm and pm.la_owned(rel, mf))
    text = ""
    if f.suffix.lower() in (".md", ".json", ".py", ".sh", ".html", ".txt") or f.name in (".gitignore", ".gitattributes"):
        text = f.read_text(encoding="utf-8-sig")
    m = re.match(r"^\.claude/skills/([^/]+)/SKILL\.md$", rel)
    if m:
        ten = m.group(1)
        if ten.startswith("pccc"):
            fm = _frontmatter(text)
            if not fm.get("_co"):
                loi.append("SKILL.md thiếu frontmatter YAML (--- name/description ---)")
            else:
                if fm.get("name") != ten:
                    loi.append(f"frontmatter name='{fm.get('name')}' phải trùng tên thư mục '{ten}'")
                if not fm.get("description"):
                    loi.append("thiếu description (Claude dựa vào đây để chọn skill)")
                elif len(fm["description"]) > 1024:
                    loi.append("description > 1024 ký tự")
        elif cfg["hooks"].get("guard_namespace") == "warn" and H.co_dau_hieu_pccc(text[:4000]):
            loi.append(f"(cảnh báo) skill có nội dung PCCC nhưng thiếu tiền tố: nên đổi thành pccc-{ten}")
    m = re.match(r"^\.claude/agents/([^/]+)\.md$", rel)
    if m and m.group(1).startswith("pccc"):
        fm = _frontmatter(text)
        if not fm.get("_co"):
            loi.append("agent thiếu frontmatter YAML")
        else:
            if fm.get("name") != m.group(1):
                loi.append(f"frontmatter name='{fm.get('name')}' phải trùng tên file '{m.group(1)}'")
            if not fm.get("description"):
                loi.append("agent thiếu description")
    if f.suffix == ".json" and (owned or rel == ".claude/settings.json"):
        try:
            json.loads(text)
        except Exception as ex:
            loi.append(f"JSON không hợp lệ: {ex}")
    if f.suffix == ".py" and owned:
        try:
            with tempfile.TemporaryDirectory() as td:
                py_compile.compile(str(f), cfile=str(Path(td) / "x.pyc"), doraise=True)
        except py_compile.PyCompileError as ex:
            loi.append(f"Python lỗi cú pháp: {ex.msg}")
    if f.suffix == ".sh" and owned and "\r\n" in f.read_bytes().decode("utf-8", "replace"):
        loi.append("script .sh có CRLF → bash trên Windows/Linux sẽ lỗi; đổi sang LF")
    sh = next((s for s in mf.get("shared", []) if s["path"] == rel and s["type"] in ("md-block", "hash-block")), None)
    if sh and pm is not None:
        try:
            pm.tim_khoi(text.replace("\r\n", "\n").split("\n"), sh["type"], mf["module"])
        except Exception as ex:
            loi.append(f"khối đánh dấu PCCC bị hỏng: {ex} → khôi phục rồi chạy pccc_merge.py sync")
    return loi


def main() -> None:
    data = H.doc_input()
    if data.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        return
    root = H.thu_muc_du_an(data)
    cfg = H.doc_config(root)
    mf = H.doc_manifest(root)
    if not mf or not cfg["hooks"].get("lint_after_write", True):
        return
    rel = H.rel_path(root, (data.get("tool_input") or {}).get("file_path"))
    if not rel:
        return
    loi = kiem_tra(root, rel, mf, cfg)
    if loi:
        print(f"[PCCC lint] {rel}:\n" + "\n".join(f"- {x}" for x in loi), file=sys.stderr)
        sys.exit(2)


H.chay_an_toan(main)
