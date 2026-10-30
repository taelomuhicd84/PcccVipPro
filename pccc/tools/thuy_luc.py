#!/usr/bin/env python3
"""thuy_luc.py — Tính toán thủy lực chữa cháy & so sánh phương án (module PCCC).

Lệnh con:
  ma-sat     Tổn thất Hazen–Williams nhanh cho 1 đoạn ống
  nhom       In thông số nhóm nguy cơ sprinkler (kèm nhãn xác minh)
  sprinkler  Tính mạng sprinkler dạng nhánh (tree) cho khu vực tính toán bất lợi nhất
  hong-nuoc  Tính hệ thống họng nước chữa cháy trong nhà (lưu lượng, cột áp, giảm áp theo tầng)
  be-nuoc    Tính dung tích bể nước chữa cháy
  bom        Chọn công suất bơm, bơm bù áp và so sánh cấu hình bơm

Mọi lệnh nhận --config <file.json>; nếu file có khóa "phuong_an" (danh sách {ma, ten, thay_doi})
thì công cụ tính từng phương án, lập bảng so sánh và đề xuất phương án tối ưu chi phí.
Thêm --json để xuất kết quả máy đọc được. Ví dụ đầu vào: pccc/templates/vi-du/*.json
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pccc_common as C  # noqa: E402

V_MAX_SPRINKLER_M_S = 6.0  # [QT] ngưỡng cảnh báo vận tốc (thực hành EN 12845)


# =============================================================================== sprinkler
def _preset_nhom(nhom: Any) -> Dict[str, Any]:
    if nhom is None:
        return {}
    ds = C.tham_chieu()["sprinkler_nhom"]
    key = str(nhom)
    if key not in ds:
        raise ValueError(f"Không có nhóm '{nhom}'. Có: {[k for k in ds if not k.startswith('_')]}")
    return ds[key]


def _lay(p: Dict[str, Any], preset: Dict[str, Any], khoa: str, mac_dinh: Any = None) -> Any:
    if p.get(khoa) is not None:
        return p[khoa]
    if khoa in preset:
        return C.gia_tri(preset[khoa])
    return mac_dinh


def tinh_sprinkler(p: Dict[str, Any]) -> Dict[str, Any]:
    canh_bao: List[str] = []
    preset = _preset_nhom(p.get("nhom"))
    for k in ("cuong_do_l_s_m2", "dien_tich_tinh_toan_m2", "luu_luong_min_l_s", "thoi_gian_phut",
              "dien_tich_1_dau_max_m2", "khoang_cach_max_m"):
        if p.get(k) is None and k in preset:
            cb = C.canh_bao_nhan(k, preset[k])
            if cb:
                canh_bao.append(cb)

    cd = float(_lay(p, preset, "cuong_do_l_s_m2"))
    a_tt = float(_lay(p, preset, "dien_tich_tinh_toan_m2"))
    q_min_tc = float(_lay(p, preset, "luu_luong_min_l_s", 0.0))
    t_phut = float(_lay(p, preset, "thoi_gian_phut", 60))
    a_max = _lay(p, preset, "dien_tich_1_dau_max_m2")
    l_max = _lay(p, preset, "khoang_cach_max_m")

    k = float(p.get("k_factor", 80))
    p_min = float(p.get("ap_luc_min_dau_bar", 0.5))
    s = float(p["khoang_cach_dau_tren_nhanh_m"])
    lb = float(p["khoang_cach_giua_nhanh_m"])
    cc = float(p.get("C", 120))
    bang = p.get("bang_ong", "sch40")
    hs_pk = float(p.get("he_so_phu_kien", 1.1))

    a_s = s * lb
    if a_max is not None and a_s > float(a_max) + 1e-9:
        canh_bao.append(f"❌ Diện tích bảo vệ 1 đầu {a_s:.2f} m² > tối đa {a_max} m²")
    if l_max is not None and max(s, lb) > float(l_max) + 1e-9:
        canh_bao.append(f"❌ Khoảng cách đầu phun {max(s, lb):.2f} m > tối đa {l_max} m")

    d_lpm_m2 = cd * 60.0  # l/(s·m²) -> L/(min·m²)
    q_dau_min = max(d_lpm_m2 * a_s, k * math.sqrt(p_min))
    n_yc = math.ceil(a_tt / a_s - 1e-9)
    n_h = int(p.get("so_dau_moi_nhanh") or math.ceil(1.2 * math.sqrt(a_tt) / s - 1e-9))
    n_h = max(1, min(n_h, n_yc))
    n_b = int(p.get("so_nhanh") or math.ceil(n_yc / n_h - 1e-9))

    # --- ống nhánh, đi từ đầu xa nhất về ống chính
    ds_ong_nhanh = p.get("ong_nhanh") or ["DN25"]
    if isinstance(ds_ong_nhanh, str):
        ds_ong_nhanh = [ds_ong_nhanh]
    pi = (q_dau_min / k) ** 2
    qi = k * math.sqrt(pi)
    q_cd = qi
    bang_nhanh = [{"dau": 1, "p_bar": pi, "q_lpm": qi}]
    v_max_thuc = 0.0
    for i in range(1, n_h):
        dn = ds_ong_nhanh[min(i - 1, len(ds_ong_nhanh) - 1)]
        d = C.duong_kinh_trong_mm(dn, bang)
        dp = C.ma_sat_hw_bar_m(q_cd, d, cc) * s * hs_pk
        v = C.van_toc_m_s(q_cd, d)
        v_max_thuc = max(v_max_thuc, v)
        bang_nhanh[-1].update({"dn_doan_ke": dn, "Q_doan_lpm": q_cd, "v_m_s": v, "dp_bar": dp})
        pi = pi + dp
        qi = k * math.sqrt(pi)
        q_cd += qi
        bang_nhanh.append({"dau": i + 1, "p_bar": pi, "q_lpm": qi})

    kn = p.get("ong_nhanh_ket_noi") or {}
    dn_kn = kn.get("dn", ds_ong_nhanh[min(n_h - 1, len(ds_ong_nhanh) - 1)])
    d_kn = C.duong_kinh_trong_mm(dn_kn, bang)
    dai_kn = float(kn.get("dai_m", s / 2.0))
    chenh_kn = float(kn.get("chenh_cao_m", 0.0))  # dương: nhánh cao hơn ống chính
    dp_kn = C.ma_sat_hw_bar_m(q_cd, d_kn, cc) * dai_kn * hs_pk + C.m_sang_bar(chenh_kn)
    v_max_thuc = max(v_max_thuc, C.van_toc_m_s(q_cd, d_kn))
    bang_nhanh[-1].update({"dn_doan_ke": dn_kn, "Q_doan_lpm": q_cd, "v_m_s": C.van_toc_m_s(q_cd, d_kn),
                           "dp_bar": dp_kn})
    q_nhanh = q_cd
    p_nhanh_tai_chinh = pi + dp_kn
    k_nhanh = q_nhanh / math.sqrt(p_nhanh_tai_chinh)

    # --- ống chính nhánh (cross main)
    ds_ong_chinh = p.get("ong_chinh_nhanh") or "DN65"
    if isinstance(ds_ong_chinh, str):
        ds_ong_chinh = [ds_ong_chinh]
    p_j = p_nhanh_tai_chinh
    q_main = q_nhanh
    bang_chinh = [{"nhanh": 1, "P_bar": p_j, "Q_nhanh_lpm": q_nhanh, "Q_cong_don_lpm": q_main}]
    for j in range(1, n_b):
        dn = ds_ong_chinh[min(j - 1, len(ds_ong_chinh) - 1)]
        d = C.duong_kinh_trong_mm(dn, bang)
        dp = C.ma_sat_hw_bar_m(q_main, d, cc) * lb * hs_pk
        v = C.van_toc_m_s(q_main, d)
        v_max_thuc = max(v_max_thuc, v)
        bang_chinh[-1].update({"dn_doan_ke": dn, "v_m_s": v, "dp_bar": dp})
        p_j += dp
        q_j = k_nhanh * math.sqrt(p_j)
        q_main += q_j
        bang_chinh.append({"nhanh": j + 1, "P_bar": p_j, "Q_nhanh_lpm": q_j, "Q_cong_don_lpm": q_main})

    q_spr_lps = C.lps(q_main)
    q_tk_lps = max(q_spr_lps, q_min_tc)
    if q_min_tc > q_spr_lps:
        canh_bao.append(f"ℹ️ Lưu lượng tính toán {q_spr_lps:.1f} l/s < lưu lượng tối thiểu theo nhóm "
                        f"{q_min_tc:g} l/s → lấy {q_min_tc:g} l/s cho bơm/bể")
    q_bo_sung = float(p.get("luu_luong_bo_sung_l_s", 0.0))
    q_bom_lps = q_tk_lps + q_bo_sung

    # --- ống cấp từ trạm bơm tới điểm vào khu vực tính toán (bảo thủ: tính với Q bơm)
    oc = p.get("ong_cap") or {"dn": "DN100", "dai_tuong_duong_m": 50}
    d_oc = C.duong_kinh_trong_mm(oc["dn"], bang)
    dp_oc = C.ma_sat_hw_bar_m(C.lpm(q_bom_lps), d_oc, cc) * float(oc.get("dai_tuong_duong_m", 50))
    v_oc = C.van_toc_m_s(C.lpm(q_bom_lps), d_oc)
    v_max_thuc = max(v_max_thuc, v_oc)
    dp_van = float(p.get("ton_that_cum_van_bar", 0.3))
    h_tinh = float(p.get("chenh_cao_m", 0.0))
    p_bom = p_j + dp_oc + dp_van + C.m_sang_bar(h_tinh)
    p_max_lv = float(p.get("ap_luc_lam_viec_max_bar", 12.0))
    if p_bom > p_max_lv:
        canh_bao.append(f"❌ Áp lực bơm {p_bom:.2f} bar > áp lực làm việc cho phép {p_max_lv} bar → phân vùng/van giảm áp")
    if v_max_thuc > V_MAX_SPRINKLER_M_S:
        canh_bao.append(f"⚠️ Vận tốc lớn nhất {v_max_thuc:.2f} m/s > {V_MAX_SPRINKLER_M_S} m/s [QT] → cân nhắc tăng cỡ ống")

    so_dau = n_b * n_h
    cd_dat = q_spr_lps / (so_dau * a_s)
    if cd_dat + 1e-9 < cd:
        canh_bao.append(f"❌ Cường độ đạt {cd_dat:.4f} < yêu cầu {cd} l/(s·m²)")
    the_tich = q_tk_lps * t_phut * 60.0 / 1000.0

    tom_tat = {
        "Q_sprinkler_l_s": q_spr_lps,
        "Q_thiet_ke_l_s": q_tk_lps,
        "Q_bom_l_s": q_bom_lps,
        "P_bom_bar": p_bom,
        "H_bom_m": C.bar_sang_m(p_bom),
        "v_max_m_s": v_max_thuc,
        "the_tich_nuoc_m3": the_tich,
        "so_dau_hoat_dong": so_dau,
    }
    return {
        "loai": "sprinkler",
        "dau_vao": {"cuong_do_l_s_m2": cd, "dien_tich_tinh_toan_m2": a_tt, "luu_luong_min_l_s": q_min_tc,
                    "thoi_gian_phut": t_phut, "k_factor": k, "ap_luc_min_dau_bar": p_min,
                    "dien_tich_1_dau_m2": a_s, "C": cc, "bang_ong": bang, "he_so_phu_kien": hs_pk},
        "q_dau_min_lpm": q_dau_min,
        "so_dau_yeu_cau": n_yc,
        "so_dau_moi_nhanh": n_h,
        "so_nhanh": n_b,
        "bang_nhanh": bang_nhanh,
        "K_nhanh": k_nhanh,
        "bang_ong_chinh": bang_chinh,
        "ong_cap": {"dn": oc["dn"], "dp_bar": dp_oc, "v_m_s": v_oc},
        "cuong_do_dat_l_s_m2": cd_dat,
        "tom_tat": tom_tat,
        "canh_bao": canh_bao,
        "_tham_so": p,
    }


def in_sprinkler(r: Dict[str, Any]) -> str:
    dv = r["dau_vao"]
    out = [f"## Sprinkler — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- Cường độ yêu cầu {dv['cuong_do_l_s_m2']} l/(s·m²); diện tích tính toán {dv['dien_tich_tinh_toan_m2']:g} m²; "
           f"K={dv['k_factor']:g}; diện tích/đầu {dv['dien_tich_1_dau_m2']:.2f} m²",
           f"- Đầu xa nhất: q={r['q_dau_min_lpm']:.1f} L/min, p={r['bang_nhanh'][0]['p_bar']:.3f} bar; "
           f"bố trí {r['so_nhanh']} nhánh × {r['so_dau_moi_nhanh']} đầu = {r['tom_tat']['so_dau_hoat_dong']} đầu "
           f"(yêu cầu ≥ {r['so_dau_yeu_cau']})", "", "**Ống nhánh bất lợi nhất (từ đầu xa nhất):**", ""]
    out.append(C.bang_markdown(["Đầu", "p (bar)", "q (L/min)", "Đoạn kế", "Q đoạn (L/min)", "v (m/s)", "Δp (bar)"],
                               [[x["dau"], x["p_bar"], x["q_lpm"], x.get("dn_doan_ke"), x.get("Q_doan_lpm"),
                                 x.get("v_m_s"), x.get("dp_bar")] for x in r["bang_nhanh"]]))
    out += ["", f"K tương đương của nhánh = {r['K_nhanh']:.1f} L/min/bar^0,5", "", "**Ống chính nhánh:**", ""]
    out.append(C.bang_markdown(["Nhánh", "P (bar)", "Q nhánh (L/min)", "Q cộng dồn (L/min)", "Đoạn kế", "v (m/s)", "Δp (bar)"],
                               [[x["nhanh"], x["P_bar"], x["Q_nhanh_lpm"], x["Q_cong_don_lpm"], x.get("dn_doan_ke"),
                                 x.get("v_m_s"), x.get("dp_bar")] for x in r["bang_ong_chinh"]]))
    t = r["tom_tat"]
    out += ["", f"- Ống cấp {r['ong_cap']['dn']}: Δp={r['ong_cap']['dp_bar']:.3f} bar, v={r['ong_cap']['v_m_s']:.2f} m/s",
            f"- **Q sprinkler = {t['Q_sprinkler_l_s']:.2f} l/s; Q thiết kế = {t['Q_thiet_ke_l_s']:.2f} l/s; "
            f"Q bơm = {t['Q_bom_l_s']:.2f} l/s; P bơm = {t['P_bom_bar']:.2f} bar ({t['H_bom_m']:.1f} m)**",
            f"- Cường độ đạt được {r['cuong_do_dat_l_s_m2']:.4f} l/(s·m²); thể tích nước {t['the_tich_nuoc_m3']:.1f} m³ "
            f"({dv['thoi_gian_phut']:g} phút)"]
    if r["canh_bao"]:
        out += ["", "**Cảnh báo / ghi chú:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== họng nước
def ap_luc_tai_hong_bar(q_lps: float, d_lang_mm: float = 13.0, dai_voi_m: float = 20.0,
                        d_voi_mm: float = 51.0, c_voi: float = 140.0, cd_lang: float = 0.97) -> Dict[str, float]:
    """Áp lực cần tại van họng = áp lực lăng + ma sát vòi (Hazen–Williams). [VL]"""
    a = math.pi * (d_lang_mm / 1000.0) ** 2 / 4.0
    v = (q_lps / 1000.0) / (cd_lang * a)
    h_lang = v * v / (2 * C.G)
    p_voi = C.ma_sat_hw_bar_m(C.lpm(q_lps), d_voi_mm, c_voi) * dai_voi_m
    p = C.m_sang_bar(h_lang) + p_voi
    return {"p_bar": p, "p_lang_bar": C.m_sang_bar(h_lang), "p_voi_bar": p_voi, "v_lang_m_s": v}


def tinh_hong_nuoc(p: Dict[str, Any]) -> Dict[str, Any]:
    canh_bao: List[str] = []
    n = int(p.get("so_tia", 1))
    q_tia = float(p.get("luu_luong_tia_l_s", 2.5))
    q = n * q_tia
    if p.get("ap_luc_hong_bar") is not None:
        p_hong = float(p["ap_luc_hong_bar"])
        chi_tiet_hong = None
    else:
        lv = p.get("lang_voi", {})
        chi_tiet_hong = ap_luc_tai_hong_bar(q_tia, float(lv.get("d_lang_mm", 13)), float(lv.get("dai_voi_m", 20)),
                                            float(lv.get("d_voi_mm", 51)), float(lv.get("C_voi", 140)))
        p_hong = chi_tiet_hong["p_bar"]
        canh_bao.append("[DC] Áp lực tại họng tính từ lăng/vòi giả định — kiểm tra chiều cao cột nước đặc yêu cầu "
                        "theo quy chuẩn/tiêu chuẩn áp dụng")
    cc = float(p.get("C", 120))
    bang = p.get("bang_ong", "sch40")
    v_max = float(p.get("van_toc_max_m_s", 3.0))
    tong_dp = 0.0
    chi_tiet = []
    v_lon = 0.0
    for doan in p.get("duong_ong", [{"dn": "DN100", "dai_m": 60}]):
        d = C.duong_kinh_trong_mm(doan["dn"], bang)
        q_doan = float(doan.get("luu_luong_l_s", q))
        dp = C.ma_sat_hw_bar_m(C.lpm(q_doan), d, cc) * float(doan["dai_m"]) * (1 + float(doan.get("he_so_cuc_bo", 0.2)))
        v = C.van_toc_m_s(C.lpm(q_doan), d)
        v_lon = max(v_lon, v)
        tong_dp += dp
        chi_tiet.append({"dn": doan["dn"], "dai_m": doan["dai_m"], "Q_l_s": q_doan, "v_m_s": v, "dp_bar": dp})
    if v_lon > v_max:
        canh_bao.append(f"⚠️ Vận tốc {v_lon:.2f} m/s > {v_max} m/s [DC/thực hành] → tăng cỡ ống")
    h_tinh = float(p.get("chenh_cao_m", 0.0))
    dp_khac = float(p.get("ton_that_khac_bar", 0.2))
    p_bom = p_hong + tong_dp + dp_khac + C.m_sang_bar(h_tinh)

    # kiểm tra áp lực tĩnh tại các tầng (bơm chạy ở điểm đóng van ~ hệ số x áp định mức)
    hs_dong_van = float(p.get("he_so_ap_dong_van", 1.2))
    p_max_hong = float(p.get("ap_luc_max_hong_bar", 4.5))
    tang = []
    if p.get("so_tang") and p.get("chieu_cao_tang_m"):
        z0 = float(p.get("cao_do_hong_tang_1_m", 1.25))
        for i in range(int(p["so_tang"])):
            z = z0 + i * float(p["chieu_cao_tang_m"])
            p_t = hs_dong_van * p_bom - C.m_sang_bar(z)
            tang.append({"tang": i + 1, "z_m": z, "p_tinh_bar": p_t, "can_giam_ap": p_t > p_max_hong})
        so_can = sum(1 for x in tang if x["can_giam_ap"])
        if so_can:
            canh_bao.append(f"⚠️ {so_can} tầng có áp lực tĩnh > {p_max_hong} bar [DC] → van giảm áp/màng tiết lưu "
                            f"hoặc phân vùng áp lực")
    tom_tat = {"Q_l_s": q, "P_bom_bar": p_bom, "H_bom_m": C.bar_sang_m(p_bom), "v_max_m_s": v_lon,
               "so_tang_can_giam_ap": sum(1 for x in tang if x["can_giam_ap"])}
    return {"loai": "hong_nuoc", "so_tia": n, "luu_luong_tia_l_s": q_tia, "p_hong_bar": p_hong,
            "chi_tiet_hong": chi_tiet_hong, "duong_ong": chi_tiet, "ton_that_ong_bar": tong_dp,
            "tang": tang, "tom_tat": tom_tat, "canh_bao": canh_bao, "_tham_so": p}


def in_hong_nuoc(r: Dict[str, Any]) -> str:
    t = r["tom_tat"]
    out = [f"## Họng nước chữa cháy trong nhà — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- {r['so_tia']} tia × {r['luu_luong_tia_l_s']:g} l/s = **{t['Q_l_s']:.2f} l/s**; áp lực yêu cầu tại họng "
           f"bất lợi {r['p_hong_bar']:.2f} bar"]
    if r["chi_tiet_hong"]:
        c = r["chi_tiet_hong"]
        out.append(f"  (lăng {c['p_lang_bar']:.2f} bar + vòi {c['p_voi_bar']:.3f} bar; v lăng {c['v_lang_m_s']:.1f} m/s)")
    out += ["", C.bang_markdown(["Đoạn", "Dài (m)", "Q (l/s)", "v (m/s)", "Δp (bar)"],
                                [[x["dn"], x["dai_m"], x["Q_l_s"], x["v_m_s"], x["dp_bar"]] for x in r["duong_ong"]]),
            "", f"- **Áp lực bơm yêu cầu {t['P_bom_bar']:.2f} bar ({t['H_bom_m']:.1f} m)**"]
    if r["tang"]:
        can = [str(x["tang"]) for x in r["tang"] if x["can_giam_ap"]]
        out.append(f"- Tầng cần giảm áp: {', '.join(can) if can else 'không'}")
    if r["canh_bao"]:
        out += ["", "**Cảnh báo / ghi chú:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== bể nước
def tinh_be_nuoc(p: Dict[str, Any]) -> Dict[str, Any]:
    canh_bao: List[str] = []
    dong = []
    tong = 0.0
    t_max_h = 0.0
    for tp in p.get("thanh_phan", []):
        q = float(tp["luu_luong_l_s"])
        if "thoi_gian_gio" in tp:
            t_h = float(tp["thoi_gian_gio"])
        else:
            t_h = float(tp.get("thoi_gian_phut", 60)) / 60.0
        v = q * 3.6 * t_h
        t_max_h = max(t_max_h, t_h)
        tong += v
        dong.append({"ten": tp.get("ten", "?"), "Q_l_s": q, "t_gio": t_h, "V_m3": v, "ghi_chu": tp.get("ghi_chu", "")})
    q_bu = float(p.get("bu_nuoc_trong_khi_chay_l_s", 0.0))
    v_bu = q_bu * 3.6 * t_max_h
    if q_bu > 0:
        canh_bao.append("[DC] Chỉ trừ lượng nước bổ sung khi nguồn cấp được bảo đảm liên tục trong thời gian chữa cháy "
                        "(có văn bản xác nhận của đơn vị cấp nước)")
    v_yc = max(tong - v_bu, 0.0)
    kt = p.get("kich_thuoc", {})
    h_nuoc = float(kt.get("chieu_cao_nuoc_m", 2.5))
    h_tu_do = float(kt.get("khoang_trong_m", 0.3))
    ty_le = float(kt.get("ty_le_dai_rong", 2.0))
    dt = v_yc / h_nuoc if h_nuoc > 0 else 0
    rong = math.sqrt(dt / ty_le) if dt > 0 else 0
    dai = ty_le * rong
    goi_y = {"dien_tich_day_m2": dt, "dai_m": math.ceil(dai * 10) / 10, "rong_m": math.ceil(rong * 10) / 10,
             "cao_thong_thuy_m": h_nuoc + h_tu_do, "so_ngan_khuyen_nghi": 2 if v_yc > 100 else 1}
    tom_tat = {"V_yeu_cau_m3": v_yc, "V_tong_m3": tong, "V_bu_m3": v_bu}
    return {"loai": "be_nuoc", "thanh_phan": dong, "tom_tat": tom_tat, "goi_y_kich_thuoc": goi_y,
            "canh_bao": canh_bao, "_tham_so": p}


def in_be_nuoc(r: Dict[str, Any]) -> str:
    t, g = r["tom_tat"], r["goi_y_kich_thuoc"]
    out = [f"## Bể nước chữa cháy — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "), "",
           C.bang_markdown(["Thành phần", "Q (l/s)", "t (giờ)", "V (m³)", "Ghi chú"],
                           [[x["ten"], x["Q_l_s"], x["t_gio"], x["V_m3"], x["ghi_chu"]] for x in r["thanh_phan"]]),
           "", f"- Tổng {t['V_tong_m3']:.1f} m³ − bổ sung trong khi cháy {t['V_bu_m3']:.1f} m³ = "
               f"**{t['V_yeu_cau_m3']:.1f} m³**",
           f"- Gợi ý: {g['dai_m']} × {g['rong_m']} m, cao thông thủy {g['cao_thong_thuy_m']:.2f} m, "
           f"{g['so_ngan_khuyen_nghi']} ngăn (để vệ sinh không mất toàn bộ dự trữ)"]
    if r["canh_bao"]:
        out += ["", "**Ghi chú:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== bơm
def he_so_du_phong_dong_co(p_truc_kw: float) -> float:
    """Hệ số dự phòng công suất động cơ theo thực hành [QT]."""
    if p_truc_kw <= 2:
        return 1.5
    if p_truc_kw <= 5:
        return 1.3
    if p_truc_kw <= 50:
        return 1.15
    return 1.1


def tinh_bom(p: Dict[str, Any], dg: Dict[str, Any] | None = None) -> Dict[str, Any]:
    dg = dg or C.don_gia(p.get("_file_don_gia"))
    q = float(p["Q_l_s"])
    h = float(p["H_m"])
    eta = float(p.get("hieu_suat", 0.65))
    p_truc = 1000 * C.G * (q / 1000.0) * h / eta / 1000.0
    p_dc = p_truc * he_so_du_phong_dong_co(p_truc)
    p_tc = C.chon_lon_hon_gan_nhat(p_dc, C.tham_chieu()["dong_co_tieu_chuan_kw"]) or p_dc
    q_bu = float(p.get("Q_bu_ap_l_s", max(0.5, round(0.02 * q, 2))))
    h_bu = float(p.get("H_bu_ap_m", h + 5.0))
    p_bu = 1000 * C.G * (q_bu / 1000.0) * h_bu / 0.45 / 1000.0
    p_bu_tc = C.chon_lon_hon_gan_nhat(p_bu * 1.3, C.tham_chieu()["dong_co_tieu_chuan_kw"]) or p_bu
    gia_dien = dg["bom_dien_tron_bo_vnd_kw"] * p_tc
    gia_diesel = dg["bom_diesel_tron_bo_vnd_kw"] * p_tc
    gia_bu = dg["bom_bu_ap_tron_bo_vnd"]
    van_hanh = p_tc * dg["gio_chay_thu_nam"] * dg["dien_nang_vnd_kwh"] * dg["so_nam_vong_doi"]
    cau_hinh = [
        {"ma": "B1", "ten": "1 bơm điện chính + 1 bơm diesel dự phòng + bơm bù áp",
         "von": gia_dien + gia_diesel + gia_bu,
         "uu": "Không phụ thuộc nguồn điện thứ 2; tin cậy khi mất điện toàn bộ",
         "nhuoc": "Cần phòng bơm thông gió, ống xả, bồn dầu; bảo dưỡng động cơ diesel"},
        {"ma": "B2", "ten": "2 bơm điện (chính + dự phòng) + bơm bù áp, 2 nguồn điện (lưới + máy phát)",
         "von": 2 * gia_dien + gia_bu,
         "uu": "Gọn, rẻ, ít bảo dưỡng; phù hợp khi có máy phát dự phòng ưu tiên cấp cho PCCC",
         "nhuoc": "Phụ thuộc máy phát/ nguồn thứ 2 (phải đảm bảo cấp điện ưu tiên, cáp chống cháy)"},
        {"ma": "B3", "ten": "2 bơm điện + 1 bơm diesel + bơm bù áp",
         "von": 2 * gia_dien + gia_diesel + gia_bu,
         "uu": "Độ tin cậy cao nhất (công trình đặc biệt quan trọng, kho lớn)",
         "nhuoc": "Chi phí và diện tích lớn nhất"},
    ]
    for ch in cau_hinh:
        ch["chi_phi_vong_doi"] = ch["von"] + van_hanh
    tom_tat = {"P_truc_kW": p_truc, "P_dong_co_kW": p_tc, "Q_l_s": q, "H_m": h, "P_bu_ap_kW": p_bu_tc}
    return {"loai": "bom", "tom_tat": tom_tat, "bom_bu_ap": {"Q_l_s": q_bu, "H_m": h_bu, "P_kW": p_bu_tc},
            "cau_hinh": cau_hinh, "canh_bao": [
                "[DC] Bơm dự phòng phải có lưu lượng, cột áp không nhỏ hơn bơm chính; nguồn điện ưu tiên/chống cháy "
                "theo TCVN 7336:2021 & QCVN 06:2022 — đối chiếu điều khoản",
                "[QT] Lưu lượng bơm bù áp ước tính 2% Q (tối thiểu 0,5 l/s), cột áp = H + 5 m — chỉnh theo rò rỉ thực tế"],
            "_tham_so": p}


def in_bom(r: Dict[str, Any]) -> str:
    t = r["tom_tat"]
    out = [f"## Bơm chữa cháy — Q={t['Q_l_s']:.2f} l/s, H={t['H_m']:.1f} m",
           f"- Công suất trục {t['P_truc_kW']:.2f} kW → động cơ tiêu chuẩn **{t['P_dong_co_kW']:g} kW**",
           f"- Bơm bù áp: Q={r['bom_bu_ap']['Q_l_s']:.2f} l/s, H={r['bom_bu_ap']['H_m']:.1f} m, ~{r['bom_bu_ap']['P_kW']:g} kW",
           "", C.bang_markdown(["Mã", "Cấu hình", "Vốn (VND)", "Vòng đời (VND)", "Ưu", "Nhược"],
                               [[c["ma"], c["ten"], float(c["von"]), float(c["chi_phi_vong_doi"]), c["uu"], c["nhuoc"]]
                                for c in r["cau_hinh"]])]
    out += ["", "**Ghi chú:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== so sánh chi phí
def chi_phi_phuong_an(r: Dict[str, Any], dg: Dict[str, Any]) -> Dict[str, Any]:
    """Ước tính chi phí để xếp hạng phương án (đơn giá giả định — chỉ so sánh tương đối)."""
    p = r.get("_tham_so", {})
    t = r["tom_tat"]
    ong = 0.0
    thieu = []
    for dn, dai in (p.get("khoi_luong_ong_m") or {}).items():
        gia = dg["ong_thep_lap_dat_vnd_m"].get(dn)
        if gia is None:
            thieu.append(dn)
            continue
        ong += gia * float(dai)
    dau = dg["dau_sprinkler_lap_dat_vnd_cai"] * float(p.get("so_dau_toan_he", 0))
    kw = None
    if "Q_bom_l_s" in t or "Q_l_s" in t:
        q = t.get("Q_bom_l_s", t.get("Q_l_s"))
        h = t.get("H_bom_m")
        if h is not None:
            b = tinh_bom({"Q_l_s": q, "H_m": h, "hieu_suat": p.get("hieu_suat_bom", 0.65)}, dg)
            kw = b["tom_tat"]["P_dong_co_kW"]
    bom = 2 * dg["bom_dien_tron_bo_vnd_kw"] * kw if kw else 0.0
    dien = (kw or 0) * dg["gio_chay_thu_nam"] * dg["dien_nang_vnd_kwh"] * dg["so_nam_vong_doi"]
    be = 0.0
    if "the_tich_nuoc_m3" in t:
        be = dg["be_nuoc_btct_vnd_m3"] * t["the_tich_nuoc_m3"]
    elif "V_yeu_cau_m3" in t:
        be = dg["be_nuoc_btct_vnd_m3"] * t["V_yeu_cau_m3"]
    return {"ong": ong, "dau_phun": dau, "bom_2_to": bom, "be": be, "dien_vong_doi": dien,
            "tong": ong + dau + bom + be + dien, "kW": kw, "thieu_don_gia": thieu}


def so_sanh(ket_qua: List[Dict[str, Any]], dg: Dict[str, Any]) -> Dict[str, Any]:
    hang = []
    for r in ket_qua:
        cp = chi_phi_phuong_an(r, dg)
        loi = [x for x in r.get("canh_bao", []) if x.startswith("❌")]
        hang.append({"ma": r["_phuong_an"]["ma"], "ten": r["_phuong_an"]["ten"], "tom_tat": r["tom_tat"],
                     "chi_phi": cp, "dat": not loi, "loi": loi})
    dat = [h for h in hang if h["dat"]]
    de_xuat = min(dat, key=lambda h: h["chi_phi"]["tong"]) if dat else None
    return {"bang": hang, "de_xuat": de_xuat["ma"] if de_xuat else None,
            "ly_do": ("Chi phí vòng đời thấp nhất trong các phương án đạt yêu cầu kỹ thuật (đơn giá giả định)"
                      if de_xuat else "Không có phương án nào đạt — xem lỗi ❌")}


def in_so_sanh(ss: Dict[str, Any]) -> str:
    if not ss["bang"]:
        return ""
    khoa = list(ss["bang"][0]["tom_tat"].keys())
    out = ["## So sánh phương án", "",
           C.bang_markdown(["PA", "Tên"] + khoa + ["kW bơm", "Chi phí ước tính (VND)", "Đạt"],
                           [[h["ma"], h["ten"]] + [h["tom_tat"][k] for k in khoa] +
                            [h["chi_phi"]["kW"], float(h["chi_phi"]["tong"]), "✅" if h["dat"] else "❌"]
                            for h in ss["bang"]]),
           "", f"**Đề xuất: {ss['de_xuat'] or '—'}** — {ss['ly_do']}",
           "> Chi phí dùng đơn giá GIẢ ĐỊNH (pccc/tools/don_gia_mac_dinh.json) chỉ để xếp hạng tương đối; "
           "cập nhật đơn giá thực tế trước khi kết luận."]
    for h in ss["bang"]:
        if h["chi_phi"]["thieu_don_gia"]:
            out.append(f"- PA {h['ma']}: thiếu đơn giá cho {h['chi_phi']['thieu_don_gia']}")
    return "\n".join(out)


# =============================================================================== CLI
def _chay(args: argparse.Namespace, ham, ham_in) -> int:
    cfg = C.doc_cau_hinh(args)
    co_so = cfg.get("thong_so", cfg)
    co_so = {k: v for k, v in co_so.items() if k not in ("phuong_an", "ten", "_mo_ta", "_ghi_chu")}
    for k, v in vars(args).items():
        if k in ("config", "json", "func", "don_gia", "lenh") or v is None:
            continue
        co_so[k] = v
    dg = C.don_gia(args.don_gia)
    kq = C.chay_phuong_an(co_so, cfg.get("phuong_an", []), ham)
    ss = so_sanh(kq, dg) if len(kq) > 1 else None
    if args.json:
        C.in_ket_qua({"ket_qua": kq, "so_sanh": ss}, True, str)
    else:
        print(f"# {cfg.get('ten', 'Tính toán thủy lực')}\n")
        print("\n\n".join(ham_in(r) for r in kq))
        if ss:
            print("\n" + in_so_sanh(ss))
    return 0 if all(not [x for x in r.get("canh_bao", []) if x.startswith("❌")] for r in kq) else 2


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)

    def chung(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--config", help="file JSON đầu vào (có thể chứa 'phuong_an')")
        sp.add_argument("--json", action="store_true", help="xuất JSON")
        sp.add_argument("--don-gia", dest="don_gia", help="file JSON đơn giá (mặc định: don_gia_mac_dinh.json)")

    sp = sub.add_parser("ma-sat", help="tổn thất Hazen–Williams 1 đoạn ống")
    sp.add_argument("--q-l-s", type=float, required=True)
    sp.add_argument("--dn", required=True, help="VD DN100 hoặc đường kính trong mm")
    sp.add_argument("--c", type=float, default=120)
    sp.add_argument("--dai-m", type=float, default=100)
    sp.add_argument("--bang-ong", default="sch40")

    sp = sub.add_parser("nhom", help="in thông số nhóm nguy cơ sprinkler")

    sp = sub.add_parser("sprinkler", help="tính mạng sprinkler dạng nhánh")
    chung(sp)
    sp.add_argument("--nhom", help="1 | 2 | 3 | 4.1")

    sp = sub.add_parser("hong-nuoc", help="tính hệ thống họng nước trong nhà")
    chung(sp)
    sp = sub.add_parser("be-nuoc", help="tính dung tích bể")
    chung(sp)
    sp = sub.add_parser("bom", help="chọn bơm & so sánh cấu hình")
    chung(sp)
    sp.add_argument("--q-l-s", dest="Q_l_s", type=float)
    sp.add_argument("--h-m", dest="H_m", type=float)

    args = ap.parse_args(argv)
    if args.lenh == "ma-sat":
        d = C.duong_kinh_trong_mm(args.dn, args.bang_ong)
        q = C.lpm(args.q_l_s)
        r = C.ma_sat_hw_bar_m(q, d, args.c)
        print(f"d trong = {d:.2f} mm; v = {C.van_toc_m_s(q, d):.2f} m/s; "
              f"Δp = {r:.5f} bar/m = {r * 100:.3f} bar/100 m = {C.bar_sang_m(r * args.dai_m):.2f} m cột nước/{args.dai_m:g} m")
        return 0
    if args.lenh == "nhom":
        ds = C.tham_chieu()["sprinkler_nhom"]
        print(ds["_nguon"] + "\n")
        hang = []
        for k, v in ds.items():
            if k.startswith("_"):
                continue
            hang.append([k] + [f"{C.gia_tri(v[x])} [{C.nhan(v[x])}]" for x in
                               ("cuong_do_l_s_m2", "dien_tich_tinh_toan_m2", "luu_luong_min_l_s", "thoi_gian_phut",
                                "dien_tich_1_dau_max_m2", "khoang_cach_max_m")])
        print(C.bang_markdown(["Nhóm", "Cường độ l/(s·m²)", "DT tính toán m²", "Q min l/s", "t phút",
                               "DT/đầu max m²", "K/c max m"], hang))
        return 0
    if args.lenh == "sprinkler":
        return _chay(args, tinh_sprinkler, in_sprinkler)
    if args.lenh == "hong-nuoc":
        return _chay(args, tinh_hong_nuoc, in_hong_nuoc)
    if args.lenh == "be-nuoc":
        return _chay(args, tinh_be_nuoc, in_be_nuoc)
    if args.lenh == "bom":
        cfg = C.doc_cau_hinh(args)
        p = cfg.get("thong_so", cfg)
        if args.Q_l_s is not None:
            p["Q_l_s"] = args.Q_l_s
        if args.H_m is not None:
            p["H_m"] = args.H_m
        r = tinh_bom(p, C.don_gia(args.don_gia))
        C.in_ket_qua(r, args.json, in_bom)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
