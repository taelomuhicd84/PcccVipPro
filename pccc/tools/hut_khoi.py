#!/usr/bin/env python3
"""hut_khoi.py — Tính toán bảo vệ chống khói & so sánh phương án (module PCCC).

Lệnh con:
  hanh-lang  Lưu lượng hút khói hành lang/sảnh (TCVN 5687:2010 Phụ lục L — kiểm tra bản 2024)
  phong      Lưu lượng hút khói gian phòng (TCVN 5687:2010 Phụ lục L.2)
  nfpa92     Lưu lượng hút khói theo mô hình cột khói NFPA 92 (sảnh lớn/atrium — kiểm tra chéo)
  tang-ap    Lưu lượng tăng áp buồng thang/khoang đệm/giếng thang (Δp 20–50 Pa theo QCVN 06 Phụ lục D)
  ong-gio    Chọn kích thước ống gió chữ nhật theo lưu lượng & vận tốc giới hạn

Mọi lệnh nhận --config <file.json>; khóa "phuong_an" để so sánh nhiều phương án. Thêm --json để xuất JSON.
Ví dụ đầu vào: pccc/templates/vi-du/*.json
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pccc_common as C  # noqa: E402


def _tk() -> Dict[str, Any]:
    return C.tham_chieu()["chong_khoi"]


def _quat(q_m3h: float, dp_pa: float, eta: float = 0.55) -> Dict[str, float]:
    p_truc = (q_m3h / 3600.0) * dp_pa / eta / 1000.0
    p_dc = C.chon_lon_hon_gan_nhat(p_truc * 1.15, C.tham_chieu()["dong_co_tieu_chuan_kw"]) or p_truc * 1.15
    return {"P_truc_kW": p_truc, "P_dong_co_kW": p_dc}


def _so_mieng(chieu_dai_m: float, cau_hinh: str) -> Dict[str, Any]:
    gh = _tk()["chieu_dai_hanh_lang_1_mieng_hut_m"]
    l1 = C.gia_tri(gh.get(cau_hinh, gh["thang"]))
    return {"chieu_dai_1_mieng_m": l1, "so_mieng_toi_thieu": max(1, math.ceil(chieu_dai_m / l1 - 1e-9)),
            "nhan": C.nhan(gh.get(cau_hinh, gh["thang"]))}


# =============================================================================== hành lang
def tinh_hanh_lang(p: Dict[str, Any]) -> Dict[str, Any]:
    tk = _tk()
    cb: List[str] = []
    loai = p.get("loai_nha", "nha_o")  # nha_o | cong_cong
    b = float(p["B_m"])
    h = float(p["H_m"])
    n = p.get("n")
    if n is None:
        n = 1.0
        cb.append("[DC] Hệ số n mặc định 1,0 — PHẢI tra Bảng L1 TCVN 5687 theo tổng chiều rộng cánh cửa lớn")
    n = float(n)
    if loai == "nha_o":
        a = C.gia_tri(tk["he_so_cong_thuc_hanh_lang_nha_o"])
        kd = 1.0
        g = a * b * h ** 1.5 * n
        cong_thuc = f"G = {a:g}·B·H^1,5·n"
    else:
        a = C.gia_tri(tk["he_so_cong_thuc_hanh_lang_cong_cong"])
        kd = p.get("Kd")
        if kd is None:
            kd = 1.0
            cb.append("[DC] Hệ số Kd mặc định 1,0 — tra TCVN 5687 Phụ lục L theo số người thoát qua cửa")
        kd = float(kd)
        g = a * b * h ** 1.5 * n * kd
        cong_thuc = f"G = {a:g}·B·H^1,5·n·Kd"
    t = float(p.get("t_khoi_C", 300))
    if p.get("t_khoi_C") is None:
        cb.append("[DC] Nhiệt độ khói mặc định 300 °C — kiểm tra theo phương pháp áp dụng")
    rho = C.khoi_luong_rieng_khong_khi(t)
    l_m3h = g / rho
    rr = float(p.get("ty_le_ro_ri", 0.15))
    l_quat = l_m3h * (1 + rr)
    if p.get("ty_le_ro_ri") is None:
        cb.append("[QT] Cộng 15% rò rỉ ống/van đóng các tầng không cháy — tính chi tiết nếu trục phục vụ nhiều tầng")
    kq_mieng = None
    if p.get("chieu_dai_hanh_lang_m"):
        kq_mieng = _so_mieng(float(p["chieu_dai_hanh_lang_m"]), p.get("cau_hinh_hanh_lang", "thang"))
        if kq_mieng["nhan"] in ("DC", "QT"):
            cb.append(f"[{kq_mieng['nhan']}] 1 miệng hút phục vụ ≤ {kq_mieng['chieu_dai_1_mieng_m']} m hành lang — đối chiếu QCVN 06 Phụ lục D")
    v_mieng = float(p.get("van_toc_mieng_m_s", 6.0))
    so_mieng = kq_mieng["so_mieng_toi_thieu"] if kq_mieng else 1
    a_mieng = (l_quat / 3600.0) / v_mieng / so_mieng
    dp_quat = float(p.get("ap_suat_quat_pa", 600))
    quat = _quat(l_quat, dp_quat, float(p.get("hieu_suat_quat", 0.55)))
    tom_tat = {"G_kg_h": g, "L_m3_h": l_m3h, "L_quat_m3_h": l_quat, "so_mieng": so_mieng,
               "A_mieng_m2": a_mieng, "P_quat_kW": quat["P_dong_co_kW"]}
    return {"loai": "hanh_lang", "cong_thuc": cong_thuc, "B_m": b, "H_m": h, "n": n, "Kd": kd,
            "t_khoi_C": t, "rho": rho, "mieng": kq_mieng, "tom_tat": tom_tat, "canh_bao": cb, "_tham_so": p}


def in_hanh_lang(r: Dict[str, Any]) -> str:
    t = r["tom_tat"]
    out = [f"## Hút khói hành lang — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- {r['cong_thuc']} với B={r['B_m']:g} m, H={r['H_m']:g} m, n={r['n']:g}, Kd={r['Kd']:g} "
           f"→ **G = {t['G_kg_h']:.0f} kg/h**",
           f"- Khói {r['t_khoi_C']:g} °C, ρ={r['rho']:.3f} kg/m³ → L = {t['L_m3_h']:.0f} m³/h; "
           f"kể rò rỉ → **L quạt = {t['L_quat_m3_h']:.0f} m³/h**",
           f"- Số miệng hút tối thiểu {t['so_mieng']}; diện tích thông thủy mỗi miệng ≈ {t['A_mieng_m2']:.2f} m²",
           f"- Quạt (Δp giả định {r['_tham_so'].get('ap_suat_quat_pa', 600)} Pa): động cơ ≈ {t['P_quat_kW']:g} kW"]
    if r["canh_bao"]:
        out += ["", "**Ghi chú xác minh:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== gian phòng
def tinh_phong(p: Dict[str, Any]) -> Dict[str, Any]:
    tk = _tk()
    cb: List[str] = []
    pf = float(p["Pf_m"])
    y = float(p["y_m"])
    ks = float(p.get("Ks", 1.0))
    a = C.gia_tri(tk["he_so_cong_thuc_phong"])
    g = a * pf * y ** 1.5 * ks
    if pf > 12 or y > 4:
        cb.append("⚠️ Ngoài phạm vi áp dụng L.2 (Pf ≤ 12 m, y ≤ 4 m) [TC] → dùng L.3 hoặc kiểm tra chéo bằng lệnh nfpa92")
    t = float(p.get("t_khoi_C", 300))
    if p.get("t_khoi_C") is None:
        cb.append("[DC] Nhiệt độ khói mặc định 300 °C — kiểm tra theo phương pháp áp dụng")
    rho = C.khoi_luong_rieng_khong_khi(t)
    l_m3h = g / rho
    rr = float(p.get("ty_le_ro_ri", 0.15))
    l_quat = l_m3h * (1 + rr)
    bu = float(p.get("ty_le_cap_bu", 0.7))
    t_ngoai = float(p.get("t_ngoai_C", 30))
    l_bu = g * bu / C.khoi_luong_rieng_khong_khi(t_ngoai)
    cb.append("[DC] Cấp bù ≥ 70% lưu lượng khối lượng hút (cân bằng ≤ 30%) — đối chiếu QCVN 06 Phụ lục D")
    quat = _quat(l_quat, float(p.get("ap_suat_quat_pa", 600)), float(p.get("hieu_suat_quat", 0.55)))
    tom_tat = {"G_kg_h": g, "L_m3_h": l_m3h, "L_quat_m3_h": l_quat, "L_cap_bu_m3_h": l_bu,
               "P_quat_kW": quat["P_dong_co_kW"]}
    return {"loai": "phong", "Pf_m": pf, "y_m": y, "Ks": ks, "a": a, "t_khoi_C": t, "rho": rho,
            "tom_tat": tom_tat, "canh_bao": cb, "_tham_so": p}


def in_phong(r: Dict[str, Any]) -> str:
    t = r["tom_tat"]
    out = [f"## Hút khói gian phòng — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- G = {r['a']:g}·Pf·y^1,5·Ks = {r['a']:g}·{r['Pf_m']:g}·{r['y_m']:g}^1,5·{r['Ks']:g} = **{t['G_kg_h']:.0f} kg/h**",
           f"- Khói {r['t_khoi_C']:g} °C → L = {t['L_m3_h']:.0f} m³/h; L quạt (kể rò rỉ) = **{t['L_quat_m3_h']:.0f} m³/h**",
           f"- Cấp bù ≈ {t['L_cap_bu_m3_h']:.0f} m³/h; quạt hút ≈ {t['P_quat_kW']:g} kW"]
    if r["canh_bao"]:
        out += ["", "**Ghi chú xác minh:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== NFPA 92
def tinh_nfpa92(p: Dict[str, Any]) -> Dict[str, Any]:
    """Cột khói đối xứng trục (NFPA 92 — 5.5.1.1). [QT]"""
    cb = ["[QT] Mô hình NFPA 92 dùng để kiểm tra chéo/áp dụng khi được chấp thuận (SĐ1:2023 D.1.7 cho phép "
          "thay đổi yêu cầu Phụ lục D trên cơ sở thiết kế theo tiêu chuẩn được phép áp dụng)"]
    q = float(p["Q_kW"])
    chi_c = float(p.get("ty_le_doi_luu", 0.7))
    qc = chi_c * q
    z = float(p["z_m"])  # khoảng cách từ mặt cháy tới đáy lớp khói
    zl = 0.166 * qc ** 0.4
    if z > zl:
        m = 0.071 * qc ** (1 / 3) * z ** (5 / 3) + 0.0018 * qc
    else:
        m = 0.032 * qc ** 0.6 * z
    t0 = float(p.get("t_moi_truong_C", 30))
    dT = qc / (m * 1.0)
    ts = t0 + dT
    rho = C.khoi_luong_rieng_khong_khi(ts)
    v_m3s = m / rho
    kq = {"Qc_kW": qc, "z_l_m": zl, "m_kg_s": m, "dT_K": dT, "T_khoi_C": ts, "V_m3_s": v_m3s}
    # chống thủng lớp khói (plugholing)
    d_lop = p.get("chieu_day_lop_khoi_duoi_mieng_m")
    so_mieng = None
    if d_lop:
        gamma = float(p.get("gamma", 1.0))
        vmax = 4.16 * gamma * float(d_lop) ** 2.5 * (dT / (273.15 + t0)) ** 0.5
        so_mieng = max(1, math.ceil(v_m3s / vmax - 1e-9))
        kq.update({"V_max_1_mieng_m3_s": vmax, "so_mieng_toi_thieu": so_mieng})
    if v_m3s * 3600 > 0 and p.get("ap_suat_quat_pa"):
        kq["P_quat_kW"] = _quat(v_m3s * 3600, float(p["ap_suat_quat_pa"]))["P_dong_co_kW"]
    tom_tat = {"m_kg_s": m, "T_khoi_C": ts, "V_m3_h": v_m3s * 3600, "so_mieng": so_mieng}
    return {"loai": "nfpa92", "ket_qua": kq, "tom_tat": tom_tat, "canh_bao": cb, "_tham_so": p}


def in_nfpa92(r: Dict[str, Any]) -> str:
    k = r["ket_qua"]
    p = r["_tham_so"]
    out = [f"## Hút khói theo NFPA 92 — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- Q={p['Q_kW']} kW, Qc={k['Qc_kW']:.0f} kW, z={p['z_m']} m (z_l={k['z_l_m']:.2f} m)",
           f"- **m = {k['m_kg_s']:.2f} kg/s**, ΔT={k['dT_K']:.0f} K → T khói {k['T_khoi_C']:.0f} °C; "
           f"**V = {k['V_m3_s']:.2f} m³/s = {k['V_m3_s'] * 3600:.0f} m³/h**"]
    if "so_mieng_toi_thieu" in k:
        out.append(f"- Chống thủng lớp khói: V max/miệng {k['V_max_1_mieng_m3_s']:.2f} m³/s → ≥ {k['so_mieng_toi_thieu']} miệng")
    out += ["", "**Ghi chú:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== tăng áp
def tinh_tang_ap(p: Dict[str, Any]) -> Dict[str, Any]:
    tk = _tk()
    tc = C.tham_chieu()["ro_ri_cua_m2"]
    cb: List[str] = []
    dp_min = C.gia_tri(tk["ap_suat_du_min_pa"])
    dp_max = C.gia_tri(tk["ap_suat_du_max_pa"])
    dp = float(p.get("dp_thiet_ke_pa", 40))
    if not (dp_min <= dp <= dp_max):
        cb.append(f"❌ Δp thiết kế {dp:g} Pa ngoài khoảng {dp_min}–{dp_max} Pa [TC] (QCVN 06:2022 Phụ lục D)")
    a_ro_ri = 0.0
    for c in p.get("cua_dong", []):
        a = float(c["A_m2"]) if "A_m2" in c else float(tc[c["loai"]])
        a_ro_ri += a * float(c.get("so_luong", 1))
    a_ro_ri += float(p.get("ro_ri_khac_m2", 0.0))
    q_dong = 0.83 * a_ro_ri * math.sqrt(dp)  # m3/s — BS EN 12101-6 [QT]
    v_cua = float(p.get("van_toc_qua_cua_mo_m_s", C.gia_tri(tk["van_toc_qua_cua_mo_m_s"])))
    if p.get("van_toc_qua_cua_mo_m_s") is None:
        cb.append(f"[DC] Vận tốc qua cửa mở {v_cua} m/s — đối chiếu QCVN 06 Phụ lục D / tiêu chuẩn áp dụng")
    a_mo = 0.0
    for c in p.get("cua_mo", []):
        a_mo += float(c["rong_m"]) * float(c["cao_m"]) * float(c.get("so_luong", 1))
    dp_khi_mo = float(p.get("dp_con_lai_khi_mo_pa", 10))
    a_ro_ri_con = max(a_ro_ri - float(p.get("A_ro_ri_cua_dang_mo_m2", 0.0)), 0.0)
    q_mo = v_cua * a_mo + 0.83 * a_ro_ri_con * math.sqrt(dp_khi_mo) if a_mo > 0 else 0.0
    rr = float(p.get("ty_le_ro_ri_ong", 0.15))
    q_tk = max(q_dong, q_mo)
    q_quat = q_tk * (1 + rr)
    # xả áp khi mọi cửa đóng để không vượt Δp max
    q_cho_phep_dong = 0.83 * a_ro_ri * math.sqrt(dp_max)
    q_du = q_tk - q_cho_phep_dong
    a_xa = q_du / (0.83 * math.sqrt(dp_max)) if q_du > 0 else 0.0
    # lực mở cửa (NFPA 92 / EN 12101-6)
    lc = p.get("cua_kiem_tra_luc", {"rong_m": 0.9, "cao_m": 2.1, "d_m": 0.075, "F_dong_cua_N": 40})
    w, hh, dd = float(lc["rong_m"]), float(lc["cao_m"]), float(lc.get("d_m", 0.075))
    f = float(lc.get("F_dong_cua_N", 40)) + (w * w * hh * dp) / (2 * (w - dd))
    f_max = C.gia_tri(tk["luc_mo_cua_max_N"])
    if f > f_max:
        cb.append(f"❌ Lực mở cửa {f:.0f} N > {f_max} N [QT] → giảm Δp/ dùng tay nắm xa bản lề/ cửa nhỏ hơn")
    quat = _quat(q_quat * 3600, float(p.get("ap_suat_quat_pa", 400)), float(p.get("hieu_suat_quat", 0.55)))
    tom_tat = {"Q_cua_dong_m3_h": q_dong * 3600, "Q_cua_mo_m3_h": q_mo * 3600, "Q_quat_m3_h": q_quat * 3600,
               "A_xa_ap_m2": a_xa, "F_mo_cua_N": f, "P_quat_kW": quat["P_dong_co_kW"]}
    kiem_soat = p.get("kiem_soat_ap", "xa_ap")  # xa_ap | bien_tan
    if a_xa > 0 and kiem_soat == "xa_ap":
        cb.append(f"ℹ️ Khi mọi cửa đóng, lưu lượng dư → van xả áp ≈ {a_xa:.2f} m² (hoặc chọn kiem_soat_ap='bien_tan')")
    elif a_xa > 0:
        cb.append("ℹ️ Kiểm soát quá áp bằng biến tần + cảm biến chênh áp (duy trì Δp ≤ "
                  f"{dp_max:g} Pa khi mọi cửa đóng); kiểm tra thời gian đáp ứng khi cửa đóng/mở")
    tom_tat["kiem_soat_ap"] = kiem_soat
    cb.append("[QT] Công thức rò rỉ Q = 0,83·A·Δp^0,5 và diện tích khe cửa theo BS EN 12101-6")
    return {"loai": "tang_ap", "dp_pa": dp, "A_ro_ri_m2": a_ro_ri, "A_cua_mo_m2": a_mo, "v_cua_m_s": v_cua,
            "tom_tat": tom_tat, "canh_bao": cb, "_tham_so": p}


def in_tang_ap(r: Dict[str, Any]) -> str:
    t = r["tom_tat"]
    out = [f"## Tăng áp — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- Tiêu chí cửa đóng: ΣA rò rỉ = {r['A_ro_ri_m2']:.3f} m², Δp = {r['dp_pa']:g} Pa → {t['Q_cua_dong_m3_h']:.0f} m³/h",
           f"- Tiêu chí cửa mở: A mở = {r['A_cua_mo_m2']:.2f} m², v = {r['v_cua_m_s']:g} m/s → {t['Q_cua_mo_m3_h']:.0f} m³/h",
           f"- **Lưu lượng quạt (kể rò rỉ ống) = {t['Q_quat_m3_h']:.0f} m³/h**, động cơ ≈ {t['P_quat_kW']:g} kW",
           f"- Diện tích xả áp cần ≈ {t['A_xa_ap_m2']:.2f} m²; lực mở cửa ≈ {t['F_mo_cua_N']:.0f} N"]
    if r["canh_bao"]:
        out += ["", "**Ghi chú / cảnh báo:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== ống gió
def tinh_ong_gio(p: Dict[str, Any]) -> Dict[str, Any]:
    q = float(p["Q_m3_h"])
    v_max = float(p.get("van_toc_max_m_s", 12.0))
    t = float(p.get("t_C", 20))
    nham = float(p.get("do_nham_mm", 0.15))
    buoc = int(p.get("buoc_mm", 50))
    cao_max = int(p.get("cao_max_mm", 800))
    ung_vien = []
    for cao in range(200, cao_max + 1, buoc):
        for rong in range(cao, 3 * cao + 1, buoc):
            if (q / 3600.0) / (rong * cao / 1e6) > v_max:
                continue
            r = C.ton_that_ong_gio_pa_m(q, rong, cao, t, nham)
            ung_vien.append({"rong_mm": rong, "cao_mm": cao, "chu_vi_m": 2 * (rong + cao) / 1000.0, **r})
            break  # với mỗi chiều cao chỉ lấy chiều rộng nhỏ nhất thỏa vận tốc
    ung_vien.sort(key=lambda x: x["chu_vi_m"])
    chon = ung_vien[: int(p.get("so_goi_y", 4))]
    tom_tat = {"Q_m3_h": q, "goi_y_nho_nhat": f"{chon[0]['rong_mm']}x{chon[0]['cao_mm']}" if chon else None}
    return {"loai": "ong_gio", "goi_y": chon, "tom_tat": tom_tat, "canh_bao": [
        "[QT] Vận tốc giới hạn là thông số thực hành; ống gió hút khói phải đạt giới hạn chịu lửa theo vị trí (QCVN 06 Phụ lục D)"],
        "_tham_so": p}


def in_ong_gio(r: Dict[str, Any]) -> str:
    p = r["_tham_so"]
    out = [f"## Ống gió — Q={p['Q_m3_h']} m³/h, v ≤ {p.get('van_toc_max_m_s', 12)} m/s, t={p.get('t_C', 20)} °C", "",
           C.bang_markdown(["Kích thước (mm)", "v (m/s)", "R (Pa/m)", "Chu vi (m)", "Dh (m)"],
                           [[f"{x['rong_mm']}x{x['cao_mm']}", x["v_m_s"], x["r_pa_m"], x["chu_vi_m"], x["dh_m"]]
                            for x in r["goi_y"]])]
    out += ["", "**Ghi chú:**"] + [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== so sánh
def chi_phi(r: Dict[str, Any], dg: Dict[str, Any]) -> Dict[str, Any]:
    p = r.get("_tham_so", {})
    t = r["tom_tat"]
    kw = float(t.get("P_quat_kW") or 0)
    don_gia_quat = dg["quat_tang_ap_vnd_kw"] if r["loai"] == "tang_ap" else dg["quat_hut_khoi_vnd_kw"]
    quat = kw * don_gia_quat * float(p.get("so_quat", 1))
    ong = float(p.get("dien_tich_ong_gio_m2", 0)) * dg["ong_gio_ton_ma_kem_vnd_m2"]
    boc = 0.0
    for ei, m2 in (p.get("boc_chong_chay_m2") or {}).items():
        boc += float(m2) * dg["boc_chong_chay_ong_gio_vnd_m2"].get(ei, 0)
    van = float(p.get("so_van_hut_khoi", 0)) * dg["van_hut_khoi_vnd_cai"] + \
        float(p.get("so_van_ngan_chay", 0)) * dg["van_ngan_chay_vnd_cai"]
    dieu_khien = 0.0
    if r["loai"] == "tang_ap":
        if t.get("kiem_soat_ap") == "bien_tan":
            dieu_khien = kw * dg["bien_tan_vnd_kw"] + dg["cam_bien_chenh_ap_vnd"]
        elif t.get("A_xa_ap_m2", 0) > 0:
            dieu_khien = max(t["A_xa_ap_m2"], 0.1) * dg["van_xa_ap_vnd_m2"]
    return {"quat": quat, "ong": ong, "boc": boc, "van": van, "dieu_khien_ap": dieu_khien,
            "tong": quat + ong + boc + van + dieu_khien}


def so_sanh(kq: List[Dict[str, Any]], dg: Dict[str, Any]) -> Dict[str, Any]:
    hang = []
    for r in kq:
        loi = [x for x in r.get("canh_bao", []) if x.startswith("❌")]
        hang.append({"ma": r["_phuong_an"]["ma"], "ten": r["_phuong_an"]["ten"], "tom_tat": r["tom_tat"],
                     "chi_phi": chi_phi(r, dg), "dat": not loi})
    dat = [h for h in hang if h["dat"]]
    de_xuat = min(dat, key=lambda h: h["chi_phi"]["tong"]) if dat else None
    return {"bang": hang, "de_xuat": de_xuat["ma"] if de_xuat else None}


def in_so_sanh(ss: Dict[str, Any]) -> str:
    khoa = list(ss["bang"][0]["tom_tat"].keys())
    return "\n".join(["## So sánh phương án", "",
                      C.bang_markdown(["PA", "Tên"] + khoa + ["Chi phí ước tính (VND)", "Đạt"],
                                      [[h["ma"], h["ten"]] + [h["tom_tat"][k] for k in khoa] +
                                       [float(h["chi_phi"]["tong"]), "✅" if h["dat"] else "❌"] for h in ss["bang"]]),
                      "", f"**Đề xuất (chi phí thấp nhất trong PA đạt): {ss['de_xuat'] or '—'}** — đơn giá giả định, "
                          "chỉ so sánh tương đối; cân nhắc thêm tiêu chí kỹ thuật/kiến trúc trong báo cáo."])


# =============================================================================== CLI
HAM = {
    "hanh-lang": (tinh_hanh_lang, in_hanh_lang),
    "phong": (tinh_phong, in_phong),
    "nfpa92": (tinh_nfpa92, in_nfpa92),
    "tang-ap": (tinh_tang_ap, in_tang_ap),
    "ong-gio": (tinh_ong_gio, in_ong_gio),
}


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    for ten in HAM:
        sp = sub.add_parser(ten)
        sp.add_argument("--config", help="file JSON đầu vào (có thể chứa 'phuong_an')")
        sp.add_argument("--json", action="store_true")
        sp.add_argument("--don-gia", dest="don_gia")
        if ten == "ong-gio":
            sp.add_argument("--q-m3-h", dest="Q_m3_h", type=float)
            sp.add_argument("--v-max", dest="van_toc_max_m_s", type=float)
            sp.add_argument("--t-c", dest="t_C", type=float)
    args = ap.parse_args(argv)
    ham, ham_in = HAM[args.lenh]
    cfg = C.doc_cau_hinh(args)
    co_so = dict(cfg.get("thong_so", cfg))
    for k in ("phuong_an", "ten", "_ghi_chu", "_mo_ta"):
        co_so.pop(k, None)
    for k, v in vars(args).items():
        if k in ("config", "json", "don_gia", "lenh") or v is None:
            continue
        co_so[k] = v
    kq = C.chay_phuong_an(co_so, cfg.get("phuong_an", []), ham)
    ss = so_sanh(kq, C.don_gia(args.don_gia)) if len(kq) > 1 else None
    if args.json:
        C.in_ket_qua({"ket_qua": kq, "so_sanh": ss}, True, str)
    else:
        print(f"# {cfg.get('ten', 'Tính toán chống khói')}\n")
        print("\n\n".join(ham_in(r) for r in kq))
        if ss:
            print("\n" + in_so_sanh(ss))
    return 0 if all(not [x for x in r.get("canh_bao", []) if x.startswith("❌")] for r in kq) else 2


if __name__ == "__main__":
    sys.exit(main())
