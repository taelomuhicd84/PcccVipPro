"""SessionStart: in tóm tắt ngắn (≤ 7 dòng) về module PCCC vào ngữ cảnh. Fail-open."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pccc_hook_common as H  # noqa: E402


def main() -> None:
    data = H.doc_input()
    root = H.thu_muc_du_an(data)
    cfg = H.doc_config(root)
    mf = H.doc_manifest(root)
    if not mf or not cfg["hooks"].get("session_brief", True):
        return
    dong = [f"[PCCC v{mf.get('version', '?')}] Module trợ lý thiết kế PCCC sẵn sàng — nhận bản vẽ: dùng /pccc-thiet-ke "
            "(≥2 phương án/hạng mục, dẫn điều khoản + nhãn [BG/TC/DC/QT], ghi giả định)."]
    du_an_dir = root / "pccc" / "du-an"
    if du_an_dir.is_dir():
        ds = sorted((d for d in du_an_dir.iterdir() if d.is_dir() and not d.name.startswith(("_", "."))),
                    key=lambda d: d.stat().st_mtime, reverse=True)
        if ds:
            dong.append("Dự án gần đây: " + ", ".join(d.name for d in ds[:5]))
    try:
        ngay = date.fromisoformat(str(cfg.get("phien_ban_tri_thuc", "")))
        tuoi = (date.today() - ngay).days
        if tuoi > int(cfg.get("nhac_ra_soat_tri_thuc_sau_ngay", 180)):
            dong.append(f"⚠ Kho tri thức rà soát lần cuối {ngay.isoformat()} ({tuoi} ngày) — kiểm tra văn bản PCCC mới "
                        "trước khi kết luận (skill /pccc-cap-nhat-tri-thuc).")
    except Exception:
        pass
    pm = H.nap_merge(root)
    if pm is not None:
        try:
            lech = [f for f, tt in pm.kiem_tra_shared(root, pm.doc_manifest(root)) if tt != "ok"]
            if lech:
                dong.append("⚠ Tích hợp module lệch ở: " + ", ".join(lech) +
                            " → chạy `python3 pccc/integration/pccc_merge.py sync` (thường do vừa git merge/pull).")
            moi = pm._tim_pccc_new(root)
            if moi:
                dong.append(f"⚠ Còn {len(moi)} xung đột nâng cấp (*.pccc-new) chưa gộp — xem /pccc-hop-nhat.")
        except Exception:
            pass
    print("\n".join(dong[:7]))


H.chay_an_toan(main)
