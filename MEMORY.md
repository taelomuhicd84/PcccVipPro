# MEMORY.md — Chỉ mục bộ nhớ dự án

File này là **chỉ mục** (giống cơ chế MEMORY.md của Claude Code): nội dung nhớ nằm ở file con của từng module.

Quy tắc chung:
- Mỗi mục nhớ: ngày (YYYY-MM-DD) · bối cảnh · nội dung · nguồn. Chỉ ghi nối, không xóa lịch sử (gạch ~~lỗi thời~~ nếu cần).
- Không ghi bí mật (mật khẩu, khóa API) hoặc dữ liệu cá nhân của khách hàng.
- Mỗi module có khối riêng bên dưới.

<!-- pccc:begin · module pccc v1.0.0 · quản lý bởi pccc/integration/pccc_merge.py — sửa ở pccc/integration/blocks/, đừng sửa tay trong khối -->
## Module `pccc`
- Chỉ mục & ghi nhớ quan trọng: `pccc/memory/INDEX.md` (được import vào CLAUDE.md)
- Quyết định kỹ thuật/cấu trúc: `pccc/memory/quyet-dinh.md`
- Bài học thẩm duyệt & kinh nghiệm thiết kế: `pccc/memory/bai-hoc.md`
- Theo dự án: `pccc/memory/du-an/<mã-dự-án>.md`
- Quy tắc ghi: chỉ GHI NỐI (append), mỗi mục có ngày + nguồn; các file nhật ký dùng `merge=union` nên không xung đột khi hợp nhất.
<!-- pccc:end -->
