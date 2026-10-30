# Nhật ký quyết định (ghi nối — merge=union)

- 2026-10-30 · [cấu trúc] · Tổ chức thành module không gian tên `pccc` (thư mục `pccc/` + tài sản Claude tiền tố `pccc-`, hook trong `.claude/hooks/pccc/`) để hợp nhất với dự án khác không va chạm · yêu cầu người dùng
- 2026-10-30 · [cấu trúc] · File dùng chung (CLAUDE.md, STRUCTURE.md, MEMORY.md, README.md, .gitignore, .gitattributes) chỉ chứa KHỐI có đánh dấu do `pccc_merge.py` quản lý; `.claude/settings.json` gộp JSON; nguồn sự thật ở `pccc/integration/` → sau git merge chỉ cần `sync` · thiết kế hợp nhất
- 2026-10-30 · [cấu trúc] · Tên file ASCII (VD `so_do_note.html` thay cho “sơ_đồ_note.html”) để tránh lỗi chuẩn hóa Unicode NFC/NFD giữa macOS/Windows/Linux khi clone/merge · an toàn hợp nhất
- 2026-10-30 · [kỹ thuật] · Công cụ & hook chỉ dùng thư viện chuẩn Python ≥ 3.8; hook fail-open (thiếu Python/ lỗi → không chặn), tắt nhanh bằng `PCCC_HOOKS_DISABLED=1` · an toàn vận hành
- 2026-10-30 · [tri thức] · Gắn nhãn xác minh [BG]/[TC]/[DC]/[QT] cho mọi số liệu; công cụ không tự tra giới hạn quy chuẩn chưa xác minh (thoát nạn yêu cầu nhập giới hạn kèm nguồn) · tránh số liệu sai
- 2026-10-30 · [văn bản] · Ưu tiên QCVN 10:2025/BCA (hiệu lực 30/12/2025) hơn TCVN 3890:2023 cho diện phải trang bị hệ thống · tra cứu web 2026-10-30
