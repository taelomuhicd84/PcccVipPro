"""UserPromptSubmit: chỉ khi câu hỏi liên quan PCCC/hợp nhất mới thêm 1 dòng nhắc quy trình. Fail-open."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pccc_hook_common as H  # noqa: E402

TU_KHOA_PCCC = re.compile(
    r"pccc|phòng cháy|chữa cháy|thoát nạn|thoát hiểm|sprinkler|drencher|họng nước|báo cháy|hút khói|tăng áp|"
    r"ngăn cháy|khoang cháy|chịu lửa|thẩm duyệt|bản vẽ|mặt bằng|bơm chữa cháy|bể nước chữa cháy|"
    r"qcvn ?0?6|qcvn ?10|tcvn ?(3890|7336|5738|5687)|"
    r"phong chay|chua chay|thoat nan|thoat hiem|hong nuoc|bao chay|hut khoi|tang ap|ngan chay|khoang chay|ban ve")
TU_KHOA_HOP_NHAT = re.compile(r"hợp nhất|hop nhat|gộp dự án|gop du an|gộp repo|merge|tích hợp dự án|tich hop du an")


def main() -> None:
    data = H.doc_input()
    root = H.thu_muc_du_an(data)
    cfg = H.doc_config(root)
    if not cfg["hooks"].get("prompt_context", True) or H.doc_manifest(root) is None:
        return
    t = H.chuan_hoa(str(data.get("prompt", "")))
    dong = []
    if TU_KHOA_HOP_NHAT.search(t):
        dong.append("[PCCC] Hợp nhất dự án → theo /pccc-hop-nhat: chạy `python3 pccc/integration/pccc_merge.py plan "
                    "--target <thư mục>` trước; không sửa tay trong khối <!-- pccc:begin/end -->.")
    elif TU_KHOA_PCCC.search(t):
        dong.append("[PCCC] Theo quy trình /pccc-thiet-ke: dữ liệu bản vẽ → phân loại → kiểm tra từng hạng mục → "
                    "≥2 phương án có so sánh → dẫn điều khoản + nhãn [BG/TC/DC/QT] → ghi giả định; tính bằng pccc/tools.")
    if dong:
        print("\n".join(dong))


H.chay_an_toan(main)
