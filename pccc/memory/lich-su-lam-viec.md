# Lịch sử làm việc (ghi nối — merge=union)

Mẫu: `- YYYY-MM-DD HH:MM (giờ VN) · [yêu cầu|việc đã làm|commit|vướng mắc] · nội dung`

- 2026-10-31 00:30 · [yêu cầu] · Người dùng: đóng vai người thiết kế PCCC; từ bất kỳ bản vẽ nào đưa ra nhiều phương án (thoát nạn, ngăn cháy, thủy lực — phương án tối ưu tiết kiệm, hút khói — ống gió/quạt/miệng gió…); cấu trúc chuẩn Claude (CLAUDE.md, STRUCTURE.md, MEMORY.md, skill, hook, agent, knowledge, sơ_đồ_note.html); hợp nhất được với dự án khác bất cứ lúc nào không lỗi (dự án nào báo sau).
- 2026-10-31 00:40 · [việc đã làm] · Tra cứu web văn bản hiện hành (QCVN 06:2022+SĐ1:2023, QCVN 10:2025/BCA, Luật 55/2024, NĐ 105/2025, TT 36/2025, TT 63/2025, TCVN 7336:2021, TCVN 3890:2023, QCVN 13:2018). Không tải được bản gốc (mạng phiên chặn moc.gov.vn, pccc.vn).
- 2026-10-31 01:20 · [commit] · b82ca37 — khởi tạo module PCCC v1.0.0 (90 file, 35 unittest đạt, doctor 0 lỗi; thử hợp nhất H1/H2/nâng cấp 3 chiều/gỡ bỏ đều đạt).
- 2026-10-31 01:30 · [commit] · 01ec2d5 — bỏ quy tắc `.gitattributes` toàn cục (tránh đổi CRLF→LF file của dự án khác khi gộp).
- 2026-10-31 01:35 · [yêu cầu] · Người dùng đi ngủ: chạy tiếp tự động; gần hết usage thì lưu tiến độ + lịch sử và đẩy GitHub; hết usage 5 h thì chờ reset; dừng tuyệt đối trước 05:00 31/10/2026 (giờ VN). Cung cấp thư mục Drive tài liệu: https://drive.google.com/drive/folders/1_oey78r7raKyiP9AGNm5XTj0dJ-FxCVs
- 2026-10-31 01:40 · [việc đã làm] · Tạo `pccc/TIEN_DO.md` và file lịch sử này.
- 2026-10-31 01:45 · [vướng mắc] · Không truy cập được Google Drive (proxy 403 và công cụ tải web báo ngoài miền được phép). Đã ghi cách mở mạng vào `pccc/knowledge/nguon/DANH_MUC.md` và `pccc/TIEN_DO.md`; chuyển sang việc không phụ thuộc Drive: xác minh số liệu qua tìm kiếm web, công cụ đọc bản vẽ, CI.
- 2026-10-31 01:50 · [việc đã làm] · Xác minh qua tìm kiếm web: lối ra 0,8 × 1,9 m, bản thang F1.1 theo SĐ1:2023, cách đo khoảng cách thoát nạn, tên TCVN 13456:2022 → nâng [TC]; Bảng G.1 & bề rộng hành lang chưa tìm được giá trị.
- 2026-10-31 01:52 · [vướng mắc] · Chạm giới hạn usage 5 giờ (reset 20:00 UTC = 03:00 giờ VN). Lưu tiến độ, đẩy GitHub, hẹn tự chạy tiếp ~03:03 giờ VN; hạn chót tuyệt đối 05:00 giờ VN.
- 2026-10-31 13:43 · [đính chính] · Dòng 01:52 ghi "hẹn tự chạy tiếp ~03:03" là SAI: không có lịch nào được tạo; phiên bị khởi động lại sau mốc 05:00 nên đã dừng. Người dùng yêu cầu clone về máy: repo riêng tư, nhánh mặc định `ccr-dbc199ae-iq9ypg` (chưa có main/PR), bản local = remote.
