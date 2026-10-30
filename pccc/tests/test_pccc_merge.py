"""Kiểm thử hợp nhất: cài vào dự án giả, idempotent, giữ nội dung dự án chủ, nâng cấp 3 chiều, gỡ sạch."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "pccc" / "integration"))
import pccc_merge as PM  # noqa: E402

SETTINGS_KHAC = {
    "permissions": {"allow": ["Bash(npm run test:*)"], "deny": ["Read(./.env)"]},
    "hooks": {"PreToolUse": [{"matcher": "Write|Edit|MultiEdit",
                              "hooks": [{"type": "command", "command": "node scripts/check.js"}]}]},
    "env": {"FOO": "1"},
}


def tao_du_an_khac(thu_muc: Path) -> None:
    (thu_muc / ".claude" / "skills" / "bao-gia").mkdir(parents=True)
    (thu_muc / "CLAUDE.md").write_text("# Dự án Báo giá\n\nQuy tắc: trả lời ngắn gọn.\n", encoding="utf-8")
    (thu_muc / "README.md").write_bytes("# Bao gia\r\nDu an khac.\r\n".encode("utf-8"))
    (thu_muc / ".gitignore").write_bytes(b"node_modules/\r\n.env\r\n")
    (thu_muc / ".claude" / "settings.json").write_text(json.dumps(SETTINGS_KHAC, indent=4), encoding="utf-8")
    (thu_muc / ".claude" / "skills" / "bao-gia" / "SKILL.md").write_text(
        "---\nname: bao-gia\ndescription: Lập báo giá\n---\nx\n", encoding="utf-8")


def anh_chup(thu_muc: Path) -> dict:
    kq = {}
    for f in sorted(thu_muc.rglob("*")):
        if f.is_file() and ".git" not in f.parts:
            kq[f.relative_to(thu_muc).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return kq


def chay(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


class TestKhoiDanhDau(unittest.TestCase):
    mf = {"module": "pccc", "version": "9.9.9"}

    def test_chen_go_khoi_tron_vong(self):
        goc = "# A\n\nnội dung\n"
        co = PM.ap_khoi(goc, "md-block", "KHOI", self.mf)
        self.assertEqual(co.count("pccc:begin"), 1)
        self.assertEqual(PM.ap_khoi(co, "md-block", "KHOI", self.mf), co)  # idempotent
        self.assertEqual(PM.go_khoi(co, "md-block", "pccc"), goc)

    def test_cap_nhat_noi_dung_khoi_giu_phan_khac(self):
        co = PM.ap_khoi("# A\n", "md-block", "cu", self.mf) + "phần sau khối\n"
        moi = PM.ap_khoi(co, "md-block", "moi", self.mf)
        self.assertIn("moi", moi)
        self.assertNotIn("\ncu\n", moi)
        self.assertTrue(moi.endswith("phần sau khối\n"))

    def test_khoi_hong_bao_loi(self):
        hong = "<!-- pccc:begin -->\nx\n<!-- pccc:begin -->\ny\n<!-- pccc:end -->\n"
        with self.assertRaises(PM.LoiKhoi):
            PM.ap_khoi(hong, "md-block", "z", self.mf)

    def test_khoi_hash(self):
        co = PM.ap_khoi("node_modules/\n", "hash-block", "pccc/**/__pycache__/", self.mf)
        self.assertIn("# pccc:begin", co)
        self.assertEqual(PM.go_khoi(co, "hash-block", "pccc"), "node_modules/\n")


class TestSettings(unittest.TestCase):
    def test_gop_idempotent_va_go_chi_phan_cua_module(self):
        frag = json.loads((GOC / "pccc/integration/settings.fragment.json").read_text(encoding="utf-8"))
        marker = PM.doc_manifest()["hook_command_marker"]
        a, _ = PM.gop_settings(SETTINGS_KHAC, frag, marker)
        b, _ = PM.gop_settings(a, frag, marker)
        self.assertEqual(a, b)
        self.assertEqual(a["env"], {"FOO": "1"})
        self.assertIn("node scripts/check.js", json.dumps(a))
        go = PM.go_settings(a, marker, frag["permissions"], ["$schema"])
        self.assertEqual(go, SETTINGS_KHAC)


class TestCaiDat(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="pccc-test-"))
        self.dich = self.tmp / "du-an-khac"
        self.dich.mkdir()
        tao_du_an_khac(self.dich)
        self.goc_anh = anh_chup(self.dich)
        self.script = GOC / "pccc/integration/pccc_merge.py"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_plan_khong_ghi_gi(self):
        r = chay(self.script, "plan", "--target", str(self.dich))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(anh_chup(self.dich), self.goc_anh)

    def test_plan_chan_khi_settings_hong(self):
        (self.dich / ".claude/settings.json").write_text("{ hỏng", encoding="utf-8")
        r = chay(self.script, "plan", "--target", str(self.dich))
        self.assertEqual(r.returncode, 1)

    def test_install_giu_noi_dung_du_an_chu_va_idempotent(self):
        r = chay(self.script, "install", "--target", str(self.dich))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        claude = (self.dich / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertTrue(claude.startswith("# Dự án Báo giá\n\nQuy tắc: trả lời ngắn gọn.\n"))
        self.assertEqual(claude.count("pccc:begin"), 1)
        self.assertIn(b"\r\n", (self.dich / "README.md").read_bytes())  # giữ CRLF
        st = json.loads((self.dich / ".claude/settings.json").read_text(encoding="utf-8"))
        self.assertIn("node scripts/check.js", json.dumps(st))
        self.assertIn("Read(./.env)", st["permissions"]["deny"])
        self.assertEqual(st["env"], {"FOO": "1"})
        self.assertTrue((self.dich / ".claude/skills/pccc-thiet-ke/SKILL.md").exists())
        self.assertTrue((self.dich / ".claude/skills/bao-gia/SKILL.md").exists())
        truoc = {k: v for k, v in anh_chup(self.dich).items() if not k.endswith("install-lock.json")}
        r2 = chay(self.script, "install", "--target", str(self.dich))
        self.assertEqual(r2.returncode, 0)
        sau = {k: v for k, v in anh_chup(self.dich).items() if not k.endswith("install-lock.json")}
        self.assertEqual(truoc, sau, "cài lần 2 không được thay đổi gì")
        # sync trong đích cũng idempotent
        r3 = chay(self.dich / "pccc/integration/pccc_merge.py", "sync", "--target", str(self.dich))
        self.assertIn("Không có gì thay đổi", r3.stdout)
        r4 = chay(self.dich / "pccc/integration/pccc_merge.py", "check", "--target", str(self.dich))
        self.assertEqual(r4.returncode, 0, r4.stdout)

    def test_sync_sau_khi_merge_lay_ban_du_an_kia(self):
        chay(self.script, "install", "--target", str(self.dich))
        # mô phỏng: sau git merge, người dùng giữ bản CLAUDE.md/settings của dự án kia (mất khối PCCC)
        (self.dich / "CLAUDE.md").write_text("# Dự án Báo giá\n\nQuy tắc mới.\n", encoding="utf-8")
        (self.dich / ".claude/settings.json").write_text(json.dumps(SETTINGS_KHAC), encoding="utf-8")
        tool = self.dich / "pccc/integration/pccc_merge.py"
        self.assertEqual(chay(tool, "check", "--target", str(self.dich)).returncode, 1)
        chay(tool, "sync", "--target", str(self.dich))
        self.assertEqual(chay(tool, "check", "--target", str(self.dich)).returncode, 0)
        self.assertIn("Quy tắc mới.", (self.dich / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_nang_cap_ba_chieu_va_go_sach(self):
        src = self.tmp / "nguon"
        src.mkdir()
        for rel in ("pccc", ".claude"):
            shutil.copytree(GOC / rel, src / rel, ignore=shutil.ignore_patterns("__pycache__"))
        tool = src / "pccc/integration/pccc_merge.py"
        self.assertEqual(chay(tool, "install", "--target", str(self.dich)).returncode, 0)
        a = "pccc/tools/thoat_nan.py"   # chỉ nguồn đổi
        b = "pccc/tools/hut_khoi.py"    # chỉ đích đổi
        c = "pccc/tools/thuy_luc.py"    # cả hai đổi
        with open(src / a, "a", encoding="utf-8") as f:
            f.write("# nguon A\n")
        with open(self.dich / b, "a", encoding="utf-8") as f:
            f.write("# dich B\n")
        with open(src / c, "a", encoding="utf-8") as f:
            f.write("# nguon C\n")
        with open(self.dich / c, "a", encoding="utf-8") as f:
            f.write("# dich C\n")
        r = chay(tool, "install", "--target", str(self.dich))
        self.assertEqual(r.returncode, 1, "có xung đột phải trả mã 1")
        self.assertTrue((self.dich / a).read_text(encoding="utf-8").endswith("# nguon A\n"))
        self.assertTrue((self.dich / b).read_text(encoding="utf-8").endswith("# dich B\n"))
        self.assertTrue((self.dich / c).read_text(encoding="utf-8").endswith("# dich C\n"))
        self.assertTrue((self.dich / (c + ".pccc-new")).exists())
        chay(tool, "resolve", "--target", str(self.dich), c)
        self.assertFalse((self.dich / (c + ".pccc-new")).exists())
        self.assertEqual(chay(tool, "install", "--target", str(self.dich)).returncode, 0)
        # gỡ: file sửa cục bộ được giữ lại nếu không --force
        chay(tool, "uninstall", "--target", str(self.dich))
        self.assertTrue((self.dich / b).exists())
        chay(tool, "uninstall", "--target", str(self.dich), "--force")
        sau = anh_chup(self.dich)
        st_goc = self.goc_anh.pop(".claude/settings.json")
        st_sau = sau.pop(".claude/settings.json")
        self.assertEqual(sau, self.goc_anh, "gỡ xong phải trả dự án về nguyên trạng")
        self.assertEqual(json.loads((self.dich / ".claude/settings.json").read_text(encoding="utf-8")), SETTINGS_KHAC)
        self.assertTrue(st_goc and st_sau)


if __name__ == "__main__":
    unittest.main()
