"""Kiểm thử hook: đúng phạm vi, chặn đúng chỗ, fail-open khi lỗi/thiếu dữ liệu."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
RUN = GOC / ".claude/hooks/pccc/run_hook.sh"
CO_BASH = shutil.which("bash") is not None


def hook(ten: str, du_lieu, project: Path = GOC, env_them: dict | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    env.pop("PCCC_HOOKS_DISABLED", None)
    env.update(env_them or {})
    dau_vao = du_lieu if isinstance(du_lieu, str) else json.dumps(du_lieu)
    return subprocess.run(["bash", str(RUN), ten], input=dau_vao, capture_output=True, text=True, env=env)


@unittest.skipUnless(CO_BASH, "cần bash")
class TestHook(unittest.TestCase):
    def test_session_start(self):
        r = hook("session_start", {"hook_event_name": "SessionStart"})
        self.assertEqual(r.returncode, 0)
        self.assertTrue(r.stdout.startswith("[PCCC v"), r.stdout)
        self.assertLessEqual(len(r.stdout.strip().splitlines()), 7)

    def test_prompt_chi_khi_lien_quan(self):
        self.assertIn("[PCCC]", hook("prompt_context", {"prompt": "Kiểm tra thoát nạn bản vẽ này"}).stdout)
        self.assertIn("pccc-hop-nhat", hook("prompt_context", {"prompt": "hop nhat du an nay"}).stdout)
        self.assertEqual(hook("prompt_context", {"prompt": "viết hàm sắp xếp"}).stdout.strip(), "")

    def test_guard_khoi_quan_ly(self):
        trong = {"tool_name": "Edit", "tool_input": {"file_path": str(GOC / "CLAUDE.md"),
                                                     "old_string": "@pccc/MODULE.md", "new_string": "x"}}
        self.assertEqual(hook("guard_paths", trong).returncode, 2)
        ngoai = {"tool_name": "Edit", "tool_input": {"file_path": str(GOC / "CLAUDE.md"),
                                                     "old_string": "# CLAUDE.md — PcccVipPro", "new_string": "x"}}
        self.assertEqual(hook("guard_paths", ngoai).returncode, 0)
        cho_phep = hook("guard_paths", trong, env_them={"PCCC_ALLOW_BLOCK_EDIT": "1"})
        self.assertEqual(cho_phep.returncode, 0)

    def test_guard_tien_to(self):
        sai = {"tool_name": "Write", "tool_input": {"file_path": str(GOC / ".claude/skills/thoat-nan-moi/SKILL.md"),
                                                    "content": "---\nname: thoat-nan-moi\ndescription: PCCC\n---\n"}}
        self.assertEqual(hook("guard_paths", sai).returncode, 2)
        khac = {"tool_name": "Write", "tool_input": {"file_path": str(GOC / ".claude/skills/sap-xep/SKILL.md"),
                                                     "content": "---\nname: sap-xep\ndescription: sort\n---\n"}}
        self.assertEqual(hook("guard_paths", khac).returncode, 0)

    def test_fail_open(self):
        self.assertEqual(hook("guard_paths", "không phải json").returncode, 0)
        with tempfile.TemporaryDirectory() as td:
            r = hook("session_start", {}, project=Path(td))
            self.assertEqual((r.returncode, r.stdout.strip()), (0, ""))
        r = hook("prompt_context", {"prompt": "pccc"}, env_them={"PCCC_HOOKS_DISABLED": "1"})
        self.assertEqual((r.returncode, r.stdout), (0, ""))
        self.assertEqual(hook("khong_ton_tai", {}).returncode, 0)

    def test_lint_sau_khi_ghi(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shutil.copytree(GOC / "pccc/integration", root / "pccc/integration",
                            ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copy2(GOC / "pccc/config.json", root / "pccc/config.json")
            sk = root / ".claude/skills/pccc-thu/SKILL.md"
            sk.parent.mkdir(parents=True)
            sk.write_text("---\nname: sai-ten\n---\nx\n", encoding="utf-8")
            r = hook("lint_after_write", {"tool_name": "Write", "tool_input": {"file_path": str(sk)}}, project=root)
            self.assertEqual(r.returncode, 2)
            self.assertIn("phải trùng tên thư mục", r.stderr)
            sk.write_text("---\nname: pccc-thu\ndescription: Thử\n---\nx\n", encoding="utf-8")
            r = hook("lint_after_write", {"tool_name": "Write", "tool_input": {"file_path": str(sk)}}, project=root)
            self.assertEqual(r.returncode, 0, r.stderr)
            js = root / "pccc/x.json"
            js.write_text("{sai", encoding="utf-8")
            r = hook("lint_after_write", {"tool_name": "Edit", "tool_input": {"file_path": str(js)}}, project=root)
            self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
