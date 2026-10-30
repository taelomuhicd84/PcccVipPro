#!/usr/bin/env python3
"""thoat_nan.py — Kiểm tra thoát nạn từ dữ liệu đọc trên bản vẽ (module PCCC).

Lệnh con:
  duong-di   Đồ thị hành lang → khoảng cách từ từng cửa (căn hộ/phòng) tới lối ra gần nhất, tự phân loại
             "giữa các lối ra" hay "hành lang cụt" và so với giới hạn bạn nhập (tra QCVN 06:2022 Phụ lục G)
  so-nguoi   Tính số người theo diện tích/hệ số tải người hoặc số chỗ ngồi
  chieu-rong Kiểm tra tổng chiều rộng lối ra theo số người (khả năng thông qua) và chiều rộng tối thiểu
  phan-tan   Kiểm tra khoảng cách giữa các lối ra thoát nạn (bố trí phân tán)

Công cụ KHÔNG tự tra giới hạn quy chuẩn: giới hạn phải nhập kèm nguồn (tránh dùng số liệu chưa đối chiếu).
Mọi lệnh nhận --config <file.json> (có thể có "phuong_an") và --json.
"""
from __future__ import annotations

import argparse
import heapq
import math
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pccc_common as C  # noqa: E402

DoThi = Dict[str, List[Tuple[str, float]]]


# =============================================================================== đồ thị
def _xay_do_thi(p: Dict[str, Any]) -> Tuple[DoThi, Set[str], Dict[str, Tuple[str, float]]]:
    nut = {k: tuple(v) for k, v in p["nut"].items()}
    canh = list(p.get("canh", [])) + list(p.get("canh_them", []))
    g: DoThi = {k: [] for k in nut}
    for c in canh:
        a, b = c[0], c[1]
        if a not in nut or b not in nut:
            raise ValueError(f"Cạnh {c} tham chiếu nút chưa khai báo")
        w = float(c[2]) if len(c) > 2 else math.dist(nut[a], nut[b])
        g[a].append((b, w))
        g[b].append((a, w))
    loi_ra = set(p.get("loi_ra", [])) | set(p.get("loi_ra_them", []))
    for x in loi_ra:
        if x not in nut:
            raise ValueError(f"Lối ra '{x}' chưa khai báo trong 'nut'")
    cua_raw = dict(p.get("cua", {}))
    cua_raw.update(p.get("cua_them", {}))
    cua: Dict[str, Tuple[str, float]] = {}
    for ten, v in cua_raw.items():
        if isinstance(v, (list, tuple)):
            cua[ten] = (v[0], float(v[1]) if len(v) > 1 else 0.0)
        else:
            cua[ten] = (v, 0.0)
        if cua[ten][0] not in nut:
            raise ValueError(f"Cửa '{ten}' gắn vào nút chưa khai báo '{cua[ten][0]}'")
    return g, loi_ra, cua


def _dijkstra(g: DoThi, nguon: Iterable[str], bo: Optional[Set[str]] = None) -> Tuple[Dict[str, float], Dict[str, str], Dict[str, str]]:
    """Dijkstra đa nguồn từ các lối ra. Trả về khoảng cách, nút kế tiếp (về phía lối ra), lối ra đích."""
    bo = bo or set()
    d: Dict[str, float] = {}
    ke: Dict[str, str] = {}
    dich: Dict[str, str] = {}
    hang: List[Tuple[float, str, str]] = []
    for s in nguon:
        if s in bo:
            continue
        d[s] = 0.0
        dich[s] = s
        heapq.heappush(hang, (0.0, s, s))
    while hang:
        du, u, goc = heapq.heappop(hang)
        if du > d.get(u, math.inf) + 1e-12:
            continue
        for v, w in g[u]:
            if v in bo:
                continue
            nd = du + w
            if nd < d.get(v, math.inf) - 1e-12:
                d[v] = nd
                ke[v] = u
                dich[v] = goc
                heapq.heappush(hang, (nd, v, goc))
    return d, ke, dich


def _loi_ra_toi_duoc(g: DoThi, bat_dau: str, loi_ra: Set[str], bo: Set[str]) -> Set[str]:
    thay: Set[str] = set()
    ngan = [bat_dau]
    da = {bat_dau}
    while ngan:
        u = ngan.pop()
        if u in loi_ra:
            thay.add(u)
        for v, _ in g[u]:
            if v not in da and v not in bo:
                da.add(v)
                ngan.append(v)
    return thay


def tinh_duong_di(p: Dict[str, Any]) -> Dict[str, Any]:
    g, loi_ra, cua = _xay_do_thi(p)
    gh = p.get("gioi_han") or {}
    if "giua" not in gh or "cut" not in gh:
        raise ValueError("Thiếu 'gioi_han': {'giua': <m>, 'cut': <m>} — tra QCVN 06:2022 Phụ lục G và ghi 'nguon_gioi_han'")
    d_all, ke, dich = _dijkstra(g, loi_ra)
    hang = []
    for ten, (v, them) in sorted(cua.items()):
        if v in loi_ra:
            loai = "giua"
        else:
            tap: List[Set[str]] = [_loi_ra_toi_duoc(g, u, loi_ra, {v}) for u, _ in g[v]]
            co_hai_huong = any(x != y for i, a in enumerate(tap) for j, b in enumerate(tap) if i != j
                               for x in a for y in b)
            loai = "giua" if co_hai_huong else "cut"
        dist = d_all.get(v, math.inf) + them
        duong = [v]
        while duong[-1] in ke:
            duong.append(ke[duong[-1]])
        gioi_han = float(gh[loai])
        hang.append({"cua": ten, "nut": v, "loai": loai, "khoang_cach_m": dist, "gioi_han_m": gioi_han,
                     "dat": dist <= gioi_han + 1e-9, "loi_ra": dich.get(v), "duong_di": duong})
    so_loi = sum(1 for h in hang if not h["dat"])
    cb = [f"Giới hạn lấy theo: {p.get('nguon_gioi_han', 'CHƯA GHI NGUỒN — bổ sung (VD: QCVN 06:2022 Bảng G.1 [DC])')}"]
    if so_loi:
        cb.insert(0, f"❌ {so_loi} cửa vượt giới hạn khoảng cách thoát nạn")
    xa_nhat = max((h["khoang_cach_m"] for h in hang), default=0.0)
    tom_tat = {"so_cua": len(hang), "so_cua_khong_dat": so_loi, "xa_nhat_m": xa_nhat, "so_loi_ra": len(loi_ra)}
    return {"loai": "duong_di", "bang": hang, "tom_tat": tom_tat, "canh_bao": cb, "_tham_so": p}


def in_duong_di(r: Dict[str, Any]) -> str:
    ten_loai = {"giua": "giữa các lối ra", "cut": "hành lang cụt"}
    out = [f"## Khoảng cách thoát nạn — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "), "",
           C.bang_markdown(["Cửa", "Nút", "Vị trí", "Tới lối ra (m)", "Giới hạn (m)", "Đạt", "Lối ra", "Đường đi"],
                           [[h["cua"], h["nut"], ten_loai[h["loai"]], h["khoang_cach_m"], h["gioi_han_m"],
                             "✅" if h["dat"] else "❌", h["loi_ra"], "→".join(h["duong_di"])] for h in r["bang"]]),
           "", f"- Xa nhất: {r['tom_tat']['xa_nhat_m']:.1f} m; không đạt: {r['tom_tat']['so_cua_khong_dat']}/{r['tom_tat']['so_cua']}"]
    out += [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== số người
def tinh_so_nguoi(p: Dict[str, Any]) -> Dict[str, Any]:
    mat_do = C.tham_chieu()["mat_do_nguoi_m2_moi_nguoi"]
    hang = []
    cb = []
    tong = 0
    for k in p.get("khu", []):
        if "so_nguoi" in k:
            n, cach = int(k["so_nguoi"]), "theo nhiệm vụ thiết kế"
        elif "so_cho" in k:
            n, cach = int(k["so_cho"]), "theo số chỗ"
        else:
            m2 = k.get("m2_moi_nguoi")
            if m2 is None:
                m2 = mat_do[k["loai"]]
                cb.append(f"[QT] '{k.get('ten')}' dùng hệ số {m2} m²/người ({k['loai']}) — ưu tiên số liệu nhiệm vụ thiết kế")
            n, cach = math.ceil(float(k["dien_tich_m2"]) / float(m2) - 1e-9), f"{k['dien_tich_m2']} m² / {m2} m²/người"
        tong += n
        hang.append({"ten": k.get("ten", "?"), "so_nguoi": n, "cach_tinh": cach})
    return {"loai": "so_nguoi", "bang": hang, "tom_tat": {"tong_so_nguoi": tong}, "canh_bao": cb, "_tham_so": p}


def in_so_nguoi(r: Dict[str, Any]) -> str:
    out = ["## Số người tính toán", "",
           C.bang_markdown(["Khu", "Số người", "Cách tính"], [[h["ten"], h["so_nguoi"], h["cach_tinh"]] for h in r["bang"]]),
           "", f"- **Tổng: {r['tom_tat']['tong_so_nguoi']} người**"]
    out += [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== chiều rộng
def tinh_chieu_rong(p: Dict[str, Any]) -> Dict[str, Any]:
    kn = C.tham_chieu()["kha_nang_thong_qua_mm_moi_nguoi"]
    n = int(p["so_nguoi"])
    cb = []
    if p.get("nguoi_moi_m") is not None:
        w_yc = n / float(p["nguoi_moi_m"])
        cach = f"{n} người / {p['nguoi_moi_m']} người/m (nguồn: {p.get('nguon', 'chưa ghi')})"
    else:
        mm = float(p.get("mm_moi_nguoi", kn["cau_thang" if p.get("bo_phan") == "cau_thang" else "mat_bang_cua_hanh_lang"]))
        w_yc = n * mm / 1000.0
        cach = f"{n} người × {mm} mm/người"
        cb.append("[QT] Khả năng thông qua theo NFPA 101 — chỉ kiểm tra chéo; chiều rộng tối thiểu theo QCVN 06:2022 mục 3")
    thuc = [float(x) for x in p.get("chieu_rong_thuc_te_m", [])]
    w_min = float(p.get("chieu_rong_min_m", 0.0))
    nho = [x for x in thuc if x + 1e-9 < w_min]
    if nho:
        cb.insert(0, f"❌ Có lối ra rộng {nho} m < tối thiểu {w_min} m ({p.get('nguon_min', 'nguồn chưa ghi')})")
    tong = sum(thuc)
    if thuc and tong + 1e-9 < w_yc:
        cb.insert(0, f"❌ Tổng chiều rộng {tong:.2f} m < yêu cầu {w_yc:.2f} m")
    # mất 1 lối ra lớn nhất (kiểm tra độ dư — thực hành)
    if len(thuc) >= 2:
        con = tong - max(thuc)
        if con + 1e-9 < 0.5 * w_yc:
            cb.append(f"⚠️ Nếu lối ra lớn nhất bị khói chặn, còn {con:.2f} m < 50% yêu cầu [QT]")
    tom_tat = {"W_yeu_cau_m": w_yc, "W_thuc_te_m": tong, "so_loi_ra": len(thuc)}
    return {"loai": "chieu_rong", "cach_tinh": cach, "tom_tat": tom_tat, "canh_bao": cb, "_tham_so": p}


def in_chieu_rong(r: Dict[str, Any]) -> str:
    t = r["tom_tat"]
    out = [f"## Chiều rộng lối ra — {r['_phuong_an']['ma']}: {r['_phuong_an']['ten']}".rstrip(": "),
           f"- Yêu cầu: {r['cach_tinh']} = **{t['W_yeu_cau_m']:.2f} m**; thực tế {t['W_thuc_te_m']:.2f} m ({t['so_loi_ra']} lối ra)"]
    out += [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== phân tán
def tinh_phan_tan(p: Dict[str, Any]) -> Dict[str, Any]:
    l = float(p["khoang_cach_loi_ra_m"])
    cb = []
    kq = {"L_thuc_te_m": l}
    if p.get("chu_vi_m"):
        lq = 1.5 * math.sqrt(float(p["chu_vi_m"]))
        kq["L_min_1_5_can_P_m"] = lq
        kq["dat_1_5_can_P"] = l + 1e-9 >= lq
        cb.append("[DC] Tiêu chí L ≥ 1,5·√P (P: chu vi phòng/tầng) — đối chiếu QCVN 06:2022 mục 3.2")
    if p.get("duong_cheo_m"):
        he = 1 / 3 if p.get("co_sprinkler") else 1 / 2
        li = he * float(p["duong_cheo_m"])
        kq["L_min_duong_cheo_m"] = li
        kq["dat_duong_cheo"] = l + 1e-9 >= li
        cb.append("[QT] Tiêu chí 1/2 đường chéo (1/3 nếu có sprinkler) theo IBC/NFPA 101 — kiểm tra chéo")
    dat = all(v for k, v in kq.items() if k.startswith("dat_"))
    if not dat:
        cb.insert(0, "❌ Lối ra chưa đủ phân tán theo ít nhất một tiêu chí")
    return {"loai": "phan_tan", "ket_qua": kq, "tom_tat": {"dat": dat, **{k: v for k, v in kq.items() if k.startswith('L_')}},
            "canh_bao": cb, "_tham_so": p}


def in_phan_tan(r: Dict[str, Any]) -> str:
    k = r["ket_qua"]
    out = [f"## Bố trí phân tán lối ra — L thực tế {k['L_thuc_te_m']:.1f} m"]
    if "L_min_1_5_can_P_m" in k:
        out.append(f"- 1,5·√P = {k['L_min_1_5_can_P_m']:.1f} m → {'✅' if k['dat_1_5_can_P'] else '❌'}")
    if "L_min_duong_cheo_m" in k:
        out.append(f"- Theo đường chéo = {k['L_min_duong_cheo_m']:.1f} m → {'✅' if k['dat_duong_cheo'] else '❌'}")
    out += [f"- {x}" for x in r["canh_bao"]]
    return "\n".join(out)


# =============================================================================== CLI
HAM = {
    "duong-di": (tinh_duong_di, in_duong_di),
    "so-nguoi": (tinh_so_nguoi, in_so_nguoi),
    "chieu-rong": (tinh_chieu_rong, in_chieu_rong),
    "phan-tan": (tinh_phan_tan, in_phan_tan),
}


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="lenh", required=True)
    for ten in HAM:
        sp = sub.add_parser(ten)
        sp.add_argument("--config", required=True, help="file JSON đầu vào (có thể chứa 'phuong_an')")
        sp.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    ham, ham_in = HAM[args.lenh]
    cfg = C.doc_json(args.config)
    co_so = dict(cfg.get("thong_so", cfg))
    for k in ("phuong_an", "ten", "_ghi_chu", "_mo_ta"):
        co_so.pop(k, None)
    kq = C.chay_phuong_an(co_so, cfg.get("phuong_an", []), ham)
    if args.json:
        C.in_ket_qua({"ket_qua": kq}, True, str)
    else:
        print(f"# {cfg.get('ten', 'Kiểm tra thoát nạn')}\n")
        print("\n\n".join(ham_in(r) for r in kq))
        if len(kq) > 1:
            khoa = list(kq[0]["tom_tat"].keys())
            print("\n## So sánh phương án\n")
            print(C.bang_markdown(["PA", "Tên"] + khoa,
                                  [[r["_phuong_an"]["ma"], r["_phuong_an"]["ten"]] + [r["tom_tat"][k] for k in khoa]
                                   for r in kq]))
    return 0 if all(not [x for x in r.get("canh_bao", []) if x.startswith("❌")] for r in kq) else 2


if __name__ == "__main__":
    sys.exit(main())
