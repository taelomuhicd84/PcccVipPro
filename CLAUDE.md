# CLAUDE.md — PcccVipPro

> Điểm vào của Claude Code cho repo này. Repo tổ chức theo **module có không gian tên riêng** để hợp nhất với dự án khác bất cứ lúc nào mà không xung đột (xem `STRUCTURE.md`).

## Quy ước chung của repo (host)
- Trả lời bằng ngôn ngữ của người dùng (mặc định tiếng Việt); giữ nguyên ký hiệu kỹ thuật chuẩn (REI 150, EI 60, l/s, Pa…).
- Mỗi module sống trong thư mục riêng `<module>/` và đặt tên tài sản Claude bằng tiền tố riêng: `.claude/skills/<module>-*`, `.claude/agents/<module>-*`, `.claude/hooks/<module>/`.
- File dùng chung (`CLAUDE.md`, `STRUCTURE.md`, `MEMORY.md`, `README.md`, `.gitignore`, `.gitattributes`, `.claude/settings.json`) chứa **khối có đánh dấu** của từng module. Không sửa tay trong khối — sửa ở nguồn của module rồi chạy lệnh sync của module đó.
- Trước khi commit: chạy kiểm tra của từng module (PCCC: `python3 pccc/integration/pccc_doctor.py`).
- Sau mỗi lần `git merge` / `git pull` có đụng file dùng chung: chạy `python3 pccc/integration/pccc_merge.py sync`.

<!-- pccc:begin · module pccc v1.0.0 · quản lý bởi pccc/integration/pccc_merge.py — sửa ở pccc/integration/blocks/, đừng sửa tay trong khối -->
## Module PCCC — Trợ lý thiết kế Phòng cháy chữa cháy (PcccVipPro)

**Phạm vi:** chỉ áp dụng cho nhiệm vụ PCCC (đọc bản vẽ, thiết kế / rà soát / thẩm duyệt PCCC, tính toán chữa cháy – chống khói – thoát nạn) hoặc khi làm việc trong `pccc/`. Không áp các quy tắc này cho module khác của repo.

Tóm tắt bắt buộc (chi tiết trong các file import bên dưới):
1. Mỗi vấn đề/hệ thống → **≥ 2 phương án** (thường 3) + bảng so sánh + khuyến nghị có lý do.
2. Mỗi kết luận Đạt/Không đạt phải **dẫn điều khoản** kèm nhãn xác minh `[BG]` `[TC]` `[DC]` `[QT]`; không bịa số liệu.
3. Thiếu dữ liệu → ghi **giả định** (GĐ-01, GĐ-02…) và hỏi lại thông tin then chốt.
4. Tính toán bằng `pccc/tools/*.py` để tái lập được; lưu kết quả vào `pccc/du-an/<mã-dự-án>/`.

@pccc/MODULE.md
@pccc/memory/INDEX.md
<!-- pccc:end -->
