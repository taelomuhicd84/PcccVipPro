"""Tiện ích chung cho hook PCCC. Mọi lỗi → thoát 0 (fail-open) để không bao giờ làm hỏng phiên làm việc."""
from __future__ import annotations

import json
import os
import sys
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, Optional

MAC_DINH_HOOKS = {"session_brief": True, "prompt_context": True, "guard_managed_blocks": True,
                  "guard_namespace": "block", "lint_after_write": True}

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass


def doc_input() -> Dict[str, Any]:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def thu_muc_du_an(data: Dict[str, Any]) -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()).resolve()


def doc_config(root: Path) -> Dict[str, Any]:
    cfg: Dict[str, Any] = {"hooks": dict(MAC_DINH_HOOKS)}
    try:
        f = json.loads((root / "pccc" / "config.json").read_text(encoding="utf-8"))
        cfg.update({k: v for k, v in f.items() if k != "hooks"})
        cfg["hooks"].update(f.get("hooks", {}))
    except Exception:
        pass
    return cfg


def doc_manifest(root: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads((root / "pccc" / "integration" / "manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return None


def nap_merge(root: Path):
    """Nạp pccc_merge.py (dùng chung logic khối đánh dấu). Trả None nếu không có."""
    try:
        sys.path.insert(0, str(root / "pccc" / "integration"))
        import pccc_merge  # type: ignore
        return pccc_merge
    except Exception:
        return None


def rel_path(root: Path, fp: Optional[str]) -> Optional[str]:
    if not fp:
        return None
    try:
        p = Path(fp)
        if not p.is_absolute():
            p = root / p
        return p.resolve().relative_to(root).as_posix()
    except Exception:
        return None


def chuan_hoa(text: str) -> str:
    return unicodedata.normalize("NFC", text or "").lower()


def co_dau_hieu_pccc(text: str) -> bool:
    t = chuan_hoa(text)
    return any(k in t for k in ("pccc", "phòng cháy", "chữa cháy", "phong chay", "chua chay", "qcvn 06", "thoát nạn"))


def chan(ly_do: str) -> None:
    """PreToolUse: chặn thao tác và báo lý do cho Claude (exit 2 → stderr gửi cho Claude)."""
    print(ly_do, file=sys.stderr)
    sys.exit(2)


def chay_an_toan(ham: Callable[[], None]) -> None:
    try:
        ham()
    except SystemExit:
        raise
    except Exception:
        pass
    sys.exit(0)
