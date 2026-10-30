"""Kiểm thử công cụ tính toán PCCC: python3 -m unittest discover -s pccc/tests"""
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "pccc" / "tools"))

import pccc_common as C  # noqa: E402
import thuy_luc as TL  # noqa: E402
import hut_khoi as HK  # noqa: E402
import thoat_nan as TN  # noqa: E402

VI_DU = GOC / "pccc" / "templates" / "vi-du"


def _cau_hinh(ten: str) -> dict:
    return json.loads((VI_DU / ten).read_text(encoding="utf-8"))


def _chay(cfg: dict, ham):
    return C.chay_phuong_an(cfg["thong_so"], cfg.get("phuong_an", []), ham)


class TestThuyLuc(unittest.TestCase):
    def test_hazen_williams_khop_cong_thuc_he_my(self):
        # 250 gpm qua ống 4" Sch40, C=120 — đối chiếu dạng US (psi/ft) quy đổi sang bar/m
        us = 4.52 * 250 ** 1.85 / (120 ** 1.85 * 4.026 ** 4.87) * 0.0689476 / 0.3048
        si = C.ma_sat_hw_bar_m(250 * 3.785411784, C.duong_kinh_trong_mm("DN100"), 120)
        self.assertAlmostEqual(si, us, delta=us * 0.01)

    def test_sprinkler_nhom2_dat_cuong_do_va_luu_luong_min(self):
        kq = _chay(_cau_hinh("sprinkler-gara.json"), TL.tinh_sprinkler)
        self.assertEqual(len(kq), 3)
        for r in kq:
            self.assertGreaterEqual(r["cuong_do_dat_l_s_m2"] + 1e-9, 0.12)
            self.assertAlmostEqual(r["tom_tat"]["Q_thiet_ke_l_s"], 30.0)
            self.assertAlmostEqual(r["tom_tat"]["the_tich_nuoc_m3"], 108.0)
            ap = [x["p_bar"] for x in r["bang_nhanh"]]
            self.assertEqual(ap, sorted(ap), "áp lực phải tăng dần về phía ống chính")
            self.assertFalse([x for x in r["canh_bao"] if x.startswith("❌")])
        # ống lớn hơn → áp lực bơm nhỏ hơn
        self.assertLess(kq[1]["tom_tat"]["P_bom_bar"], kq[0]["tom_tat"]["P_bom_bar"])
        ss = TL.so_sanh(kq, C.don_gia())
        self.assertIn(ss["de_xuat"], {"A", "B", "C"})

    def test_sprinkler_bao_loi_khoang_cach_vuot(self):
        cfg = _cau_hinh("sprinkler-gara.json")["thong_so"]
        cfg = C.gop_sau(cfg, {"khoang_cach_dau_tren_nhanh_m": 4.5})
        r = TL.tinh_sprinkler(cfg)
        self.assertTrue([x for x in r["canh_bao"] if x.startswith("❌")])

    def test_hong_nuoc_ong_nho_ap_lon(self):
        kq = _chay(_cau_hinh("hong-nuoc-chung-cu.json"), TL.tinh_hong_nuoc)
        p = {r["_phuong_an"]["ma"]: r["tom_tat"]["P_bom_bar"] for r in kq}
        self.assertGreater(p["C"], p["A"])  # DN80 > DN100
        self.assertGreater(p["A"], p["B"])  # DN100 > DN125
        self.assertGreater(kq[0]["tom_tat"]["so_tang_can_giam_ap"], 0)

    def test_be_nuoc(self):
        kq = _chay(_cau_hinh("be-nuoc.json"), TL.tinh_be_nuoc)
        self.assertAlmostEqual(kq[0]["tom_tat"]["V_yeu_cau_m3"], 162.0)
        self.assertAlmostEqual(kq[1]["tom_tat"]["V_yeu_cau_m3"], 108.0)

    def test_bom_chon_dong_co_tieu_chuan(self):
        r = TL.tinh_bom({"Q_l_s": 35, "H_m": 70})
        self.assertEqual(r["tom_tat"]["P_dong_co_kW"], 45)
        self.assertEqual(len(r["cau_hinh"]), 3)


class TestHutKhoi(unittest.TestCase):
    def test_hanh_lang_cong_thuc(self):
        r = HK.tinh_hanh_lang({"loai_nha": "nha_o", "B_m": 1.0, "H_m": 2.1, "n": 1.0, "t_khoi_C": 300})
        self.assertAlmostEqual(r["tom_tat"]["G_kg_h"], 3420 * 2.1 ** 1.5, places=3)
        self.assertAlmostEqual(r["tom_tat"]["L_m3_h"], r["tom_tat"]["G_kg_h"] / (353 / 573.15), places=3)

    def test_phong_va_canh_bao_pham_vi(self):
        r = HK.tinh_phong({"Pf_m": 12, "y_m": 3.5})
        self.assertAlmostEqual(r["tom_tat"]["G_kg_h"], 678.8 * 12 * 3.5 ** 1.5, places=3)
        r2 = HK.tinh_phong({"Pf_m": 20, "y_m": 5})
        self.assertTrue(any("Ngoài phạm vi" in x for x in r2["canh_bao"]))

    def test_nfpa92(self):
        r = HK.tinh_nfpa92({"Q_kW": 2500, "z_m": 9.0, "chieu_day_lop_khoi_duoi_mieng_m": 2.5})
        k = r["ket_qua"]
        self.assertAlmostEqual(k["z_l_m"], 0.166 * 1750 ** 0.4, places=6)
        self.assertAlmostEqual(k["m_kg_s"], 0.071 * 1750 ** (1 / 3) * 9 ** (5 / 3) + 0.0018 * 1750, places=6)
        self.assertGreaterEqual(k["so_mieng_toi_thieu"], 1)

    def test_tang_ap(self):
        kq = _chay(_cau_hinh("tang-ap-buong-thang.json"), HK.tinh_tang_ap)
        t = kq[0]["tom_tat"]
        self.assertAlmostEqual(t["Q_cua_dong_m3_h"], 0.83 * 0.27 * math.sqrt(40) * 3600, places=3)
        self.assertAlmostEqual(t["F_mo_cua_N"], 40 + 0.9 * 0.9 * 2.1 * 40 / (2 * 0.825), places=6)
        ss = HK.so_sanh(kq, C.don_gia())
        self.assertIn(ss["de_xuat"], {"A", "B"})

    def test_tang_ap_ngoai_khoang_ap_suat(self):
        r = HK.tinh_tang_ap({"dp_thiet_ke_pa": 60, "cua_dong": [{"A_m2": 0.1}]})
        self.assertTrue([x for x in r["canh_bao"] if x.startswith("❌")])

    def test_ong_gio_van_toc(self):
        r = HK.tinh_ong_gio({"Q_m3_h": 30000, "van_toc_max_m_s": 12, "t_C": 300})
        self.assertTrue(r["goi_y"])
        self.assertTrue(all(x["v_m_s"] <= 12 + 1e-9 for x in r["goi_y"]))


class TestThoatNan(unittest.TestCase):
    def test_do_thi_phan_loai_va_phuong_an(self):
        kq = _chay(_cau_hinh("duong-di-tang-dien-hinh.json"), TN.tinh_duong_di)
        ht = {h["cua"]: h for h in kq[0]["bang"]}
        self.assertEqual(ht["CH04"]["loai"], "cut")
        self.assertEqual(ht["CH02"]["loai"], "giua")
        self.assertFalse(ht["CH05"]["dat"])
        self.assertAlmostEqual(ht["CH05"]["khoang_cach_m"], 31.5)
        pa_a = {h["cua"]: h for h in kq[1]["bang"]}
        self.assertTrue(all(h["dat"] for h in pa_a.values()))
        self.assertEqual(pa_a["CH04"]["loai"], "giua")

    def test_thieu_gioi_han_bao_loi(self):
        with self.assertRaises(ValueError):
            TN.tinh_duong_di({"nut": {"A": [0, 0], "B": [5, 0]}, "canh": [["A", "B"]], "loi_ra": ["A"], "cua": {"X": "B"}})

    def test_vong_ve_cung_mot_loi_ra_la_cut(self):
        p = {"nut": {"T": [0, 0], "A": [10, 0], "B": [10, 10], "C": [0, 10], "D": [20, 0]},
             "canh": [["T", "A"], ["A", "B"], ["B", "C"], ["C", "T"], ["A", "D"]],
             "loi_ra": ["T"], "cua": {"X": "B", "Y": "D"}, "gioi_han": {"giua": 40, "cut": 25}}
        r = TN.tinh_duong_di(p)
        loai = {h["cua"]: h["loai"] for h in r["bang"]}
        self.assertEqual(loai["X"], "cut")  # 2 hướng nhưng cùng về 1 lối ra T
        self.assertEqual(loai["Y"], "cut")  # cuối nhánh cụt

    def test_so_nguoi_va_chieu_rong(self):
        r = TN.tinh_so_nguoi(_cau_hinh("so-nguoi.json")["thong_so"])
        self.assertEqual(r["tom_tat"]["tong_so_nguoi"], 89 + 180 + 186 + 4)
        cr = TN.tinh_chieu_rong({"so_nguoi": 450, "chieu_rong_thuc_te_m": [1.0, 1.0]})
        self.assertTrue([x for x in cr["canh_bao"] if x.startswith("❌")])

    def test_phan_tan(self):
        r = TN.tinh_phan_tan({"khoang_cach_loi_ra_m": 30, "chu_vi_m": 160})
        self.assertTrue(r["tom_tat"]["dat"])


class TestDuLieu(unittest.TestCase):
    def test_nhan_xac_minh_hop_le(self):
        tc = C.tham_chieu()
        hop_le = {"BG", "TC", "DC", "QT", "VL"}

        def duyet(x):
            if isinstance(x, dict):
                if "xm" in x:
                    self.assertIn(x["xm"], hop_le)
                for v in x.values():
                    duyet(v)

        duyet(tc)
        for nhom, v in tc["sprinkler_nhom"].items():
            if nhom.startswith("_"):
                continue
            for k in ("cuong_do_l_s_m2", "luu_luong_min_l_s", "dien_tich_tinh_toan_m2", "thoi_gian_phut"):
                self.assertIn("xm", v[k], f"{nhom}.{k} thiếu nhãn")

    def test_vi_du_la_json_hop_le(self):
        for f in VI_DU.glob("*.json"):
            json.loads(f.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
