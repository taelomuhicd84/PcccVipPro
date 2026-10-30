"""pccc_common.py — Tiện ích dùng chung cho các công cụ tính toán của module PCCC.

Chỉ dùng thư viện chuẩn Python (>= 3.8) để chạy được ở mọi máy, không cần pip.
Tên file có tiền tố `pccc_` để không đụng tên module Python của dự án khác khi hợp nhất.
"""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

THU_MUC_TOOLS = Path(__file__).resolve().parent
FILE_THAM_CHIEU = THU_MUC_TOOLS / "du_lieu_tham_chieu.json"
FILE_DON_GIA = THU_MUC_TOOLS / "don_gia_mac_dinh.json"

# Nhãn mức xác minh (giống quy ước trong pccc/knowledge/00-muc-luc.md)
NHAN_XAC_MINH = {
    "BG": "đã đối chiếu bản gốc",
    "TC": "xác nhận qua nguồn thứ cấp — mở bản gốc khi ký hồ sơ",
    "DC": "ghi nhớ chuyên môn — BẮT BUỘC đối chiếu bản gốc",
    "QT": "tham khảo quốc tế/thực hành — cần lập luận khi áp dụng",
    "VL": "công thức vật lý/kỹ thuật chuẩn",
}

G = 9.80665  # m/s2
BAR_MOI_M_NUOC = 0.0980665  # 1 m cột nước ~ 0,0981 bar


def _cau_hinh_stdout_utf8() -> None:
    """Tránh lỗi in tiếng Việt trên console Windows (cp1252...)."""
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass


_cau_hinh_stdout_utf8()


# ----------------------------------------------------------------------------- JSON & tham số
def doc_json(duong_dan: Path | str) -> Any:
    with open(duong_dan, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def tham_chieu() -> Dict[str, Any]:
    return doc_json(FILE_THAM_CHIEU)


def don_gia(duong_dan: Optional[str] = None) -> Dict[str, Any]:
    return doc_json(duong_dan) if duong_dan else doc_json(FILE_DON_GIA)


def gia_tri(x: Any) -> Any:
    """Lấy giá trị từ dạng {"v": ..., "xm": ...} hoặc trả về chính nó."""
    if isinstance(x, dict) and "v" in x:
        return x["v"]
    return x


def nhan(x: Any) -> str:
    if isinstance(x, dict) and "xm" in x:
        return x["xm"]
    return ""


def gop_sau(goc: Dict[str, Any], ghi_de: Dict[str, Any]) -> Dict[str, Any]:
    """Gộp đệ quy: giá trị trong `ghi_de` thay giá trị trong `goc` (không sửa input)."""
    kq = copy.deepcopy(goc)
    for k, v in (ghi_de or {}).items():
        if isinstance(v, dict) and isinstance(kq.get(k), dict):
            kq[k] = gop_sau(kq[k], v)
        else:
            kq[k] = copy.deepcopy(v)
    return kq


def lam_tron(x: Any, so: int = 3) -> Any:
    if isinstance(x, float):
        if math.isinf(x) or math.isnan(x):
            return x
        return round(x, so)
    if isinstance(x, dict):
        return {k: lam_tron(v, so) for k, v in x.items()}
    if isinstance(x, list):
        return [lam_tron(v, so) for v in x]
    return x


def chon_lon_hon_gan_nhat(gia_tri_can: float, danh_sach: Sequence[float]) -> Optional[float]:
    for v in sorted(danh_sach):
        if v >= gia_tri_can - 1e-9:
            return v
    return None


# ----------------------------------------------------------------------------- Ống & thủy lực
def duong_kinh_trong_mm(dn: str | float, bang: str = "sch40") -> float:
    """Đường kính trong (mm) theo DN và bảng ống. Cho phép truyền số mm trực tiếp."""
    if isinstance(dn, (int, float)):
        return float(dn)
    s = str(dn).strip().upper()
    if s.replace(".", "", 1).isdigit():
        return float(s)
    bang_ong = tham_chieu()["ong_thep"].get(bang)
    if bang_ong is None:
        raise ValueError(f"Không có bảng ống '{bang}'. Có: {list(tham_chieu()['ong_thep'])}")
    if s not in bang_ong["duong_kinh_trong_mm"]:
        raise ValueError(f"Bảng '{bang}' không có {s}. Có: {list(bang_ong['duong_kinh_trong_mm'])}")
    return float(bang_ong["duong_kinh_trong_mm"][s])


def ma_sat_hw_bar_m(q_lpm: float, d_mm: float, c: float) -> float:
    """Tổn thất ma sát Hazen–Williams (bar/m), Q (L/min), d trong (mm). [VL]

    p = 6,05·10^5 · Q^1,85 / (C^1,85 · d^4,87)  — dạng SI dùng trong EN 12845 / NFPA 13.
    """
    if q_lpm <= 0:
        return 0.0
    return 6.05e5 * q_lpm ** 1.85 / (c ** 1.85 * d_mm ** 4.87)


def van_toc_m_s(q_lpm: float, d_mm: float) -> float:
    a = math.pi * (d_mm / 1000.0) ** 2 / 4.0
    return (q_lpm / 60000.0) / a if a > 0 else float("inf")


def lps(q_lpm: float) -> float:
    return q_lpm / 60.0


def lpm(q_lps: float) -> float:
    return q_lps * 60.0


def bar_sang_m(p_bar: float) -> float:
    return p_bar / BAR_MOI_M_NUOC


def m_sang_bar(h_m: float) -> float:
    return h_m * BAR_MOI_M_NUOC


# ----------------------------------------------------------------------------- Không khí & ống gió
def khoi_luong_rieng_khong_khi(t_c: float) -> float:
    """ρ ≈ 353 / T (kg/m3), T tính bằng K, áp suất khí quyển. [VL]"""
    return 353.0 / (273.15 + t_c)


def do_nhot_dong_luc_khong_khi(t_c: float) -> float:
    """Độ nhớt động lực (Pa·s) theo Sutherland. [VL]"""
    t = 273.15 + t_c
    return 1.716e-5 * (t / 273.15) ** 1.5 * (273.15 + 110.4) / (t + 110.4)


def he_so_ma_sat_darcy(re: float, do_nham_m: float, d_m: float) -> float:
    """Swamee–Jain (dòng rối) / 64/Re (chảy tầng). [VL]"""
    if re <= 0:
        return 0.0
    if re < 2300:
        return 64.0 / re
    return 0.25 / (math.log10(do_nham_m / (3.7 * d_m) + 5.74 / re ** 0.9)) ** 2


def ton_that_ong_gio_pa_m(q_m3h: float, rong_mm: float, cao_mm: float, t_c: float = 20.0,
                          do_nham_mm: float = 0.15) -> Dict[str, float]:
    """Tổn thất ma sát ống gió chữ nhật (Darcy–Weisbach, đường kính thủy lực). [VL]"""
    a, b = rong_mm / 1000.0, cao_mm / 1000.0
    dien_tich = a * b
    v = (q_m3h / 3600.0) / dien_tich
    dh = 2 * a * b / (a + b)
    rho = khoi_luong_rieng_khong_khi(t_c)
    mu = do_nhot_dong_luc_khong_khi(t_c)
    re = rho * v * dh / mu
    lam = he_so_ma_sat_darcy(re, do_nham_mm / 1000.0, dh)
    r = lam / dh * rho * v * v / 2.0
    return {"v_m_s": v, "dh_m": dh, "re": re, "lambda": lam, "r_pa_m": r, "rho": rho}


# ----------------------------------------------------------------------------- Phương án & bảng
def chay_phuong_an(co_so: Dict[str, Any], phuong_an: Iterable[Dict[str, Any]],
                   ham: Callable[[Dict[str, Any]], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Chạy hàm tính cho cấu hình cơ sở và từng phương án (ghi đè `thay_doi`)."""
    ds = list(phuong_an or [])
    if not ds:
        ds = [{"ma": "CS", "ten": "Cấu hình cơ sở", "thay_doi": {}}]
    kq = []
    for pa in ds:
        tham_so = gop_sau(co_so, pa.get("thay_doi", {}))
        r = ham(tham_so)
        r["_phuong_an"] = {"ma": pa.get("ma", "?"), "ten": pa.get("ten", ""), "ghi_chu": pa.get("ghi_chu", "")}
        kq.append(r)
    return kq


def bang_markdown(tieu_de: Sequence[str], hang: Iterable[Sequence[Any]]) -> str:
    def o(x: Any) -> str:
        if isinstance(x, float):
            if math.isinf(x):
                return "∞"
            if abs(x) >= 100:
                return f"{x:,.0f}".replace(",", " ")
            if abs(x) >= 10:
                return f"{x:.1f}"
            return f"{x:.3f}".rstrip("0").rstrip(".") if x != 0 else "0"
        if x is None:
            return "—"
        return str(x)

    dong = ["| " + " | ".join(tieu_de) + " |", "|" + "|".join(["---"] * len(tieu_de)) + "|"]
    for h in hang:
        dong.append("| " + " | ".join(o(x) for x in h) + " |")
    return "\n".join(dong)


def in_ket_qua(kq: Any, dang_json: bool, ham_in: Callable[[Any], str]) -> None:
    if dang_json:
        print(json.dumps(lam_tron(kq, 4), ensure_ascii=False, indent=2))
    else:
        print(ham_in(kq))


def canh_bao_nhan(ten: str, x: Any) -> Optional[str]:
    n = nhan(x)
    if n in ("DC", "QT"):
        return f"[{n}] {ten} = {gia_tri(x)} — {NHAN_XAC_MINH[n]}"
    return None


def doc_cau_hinh(args: Any) -> Dict[str, Any]:
    if getattr(args, "config", None):
        return doc_json(args.config)
    return {}
