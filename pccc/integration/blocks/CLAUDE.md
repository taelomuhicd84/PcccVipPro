## Module PCCC — Trợ lý thiết kế Phòng cháy chữa cháy (PcccVipPro)

**Phạm vi:** chỉ áp dụng cho nhiệm vụ PCCC (đọc bản vẽ, thiết kế / rà soát / thẩm duyệt PCCC, tính toán chữa cháy – chống khói – thoát nạn) hoặc khi làm việc trong `pccc/`. Không áp các quy tắc này cho module khác của repo.

Tóm tắt bắt buộc (chi tiết trong các file import bên dưới):
1. Mỗi vấn đề/hệ thống → **≥ 2 phương án** (thường 3) + bảng so sánh + khuyến nghị có lý do.
2. Mỗi kết luận Đạt/Không đạt phải **dẫn điều khoản** kèm nhãn xác minh `[BG]` `[TC]` `[DC]` `[QT]`; không bịa số liệu.
3. Thiếu dữ liệu → ghi **giả định** (GĐ-01, GĐ-02…) và hỏi lại thông tin then chốt.
4. Tính toán bằng `pccc/tools/*.py` để tái lập được; lưu kết quả vào `pccc/du-an/<mã-dự-án>/`.

@pccc/MODULE.md
@pccc/memory/INDEX.md
