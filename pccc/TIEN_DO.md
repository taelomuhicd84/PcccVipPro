# TIẾN ĐỘ — module PCCC (file trạng thái để tiếp tục công việc ở phiên sau)

Cập nhật lần cuối: 2026-10-31 13:43 (giờ VN, UTC+7)

## Trạng thái hiện tại
- v1.0.0 đã đẩy lên GitHub (nhánh `ccr-dbc199ae-iq9ypg`): cấu trúc đầy đủ, 13 skill, 6 agent, 4 hook, 14 file tri thức, 3 công cụ tính, hệ thống hợp nhất, 35 unittest, `pccc/so_do_note.html`.
- Đang làm: tải tài liệu gốc từ Google Drive người dùng cung cấp để đối chiếu, nâng nhãn số liệu `[DC]`/`[TC]` → `[BG]`.

## Hạn chót phiên làm việc hiện tại
- Người dùng yêu cầu: chạy liên tục đến khi hết usage tuần; **tuyệt đối không dùng token sau 05:00 sáng 31/10/2026 (giờ VN) = 22:00 UTC 30/10/2026**.
- Hết usage 5 giờ → chờ reset rồi chạy tiếp (nếu còn trước hạn chót trên).
- Gần hết usage → cập nhật file này + `pccc/memory/lich-su-lam-viec.md` rồi đẩy GitHub.

## Nguồn tài liệu gốc
- Thư mục Google Drive của người dùng: https://drive.google.com/drive/folders/1_oey78r7raKyiP9AGNm5XTj0dJ-FxCVs
- Danh mục & trạng thái: `pccc/knowledge/nguon/DANH_MUC.md`.
- ⛔ 2026-10-31 01:40: **Drive bị chặn** bởi chính sách mạng của phiên cloud (`drive.google.com`). Người dùng cần thêm `drive.google.com`, `drive.usercontent.google.com`, `docs.google.com` vào *Allowed domains* (Network access của môi trường) hoặc gửi file trực tiếp trong chat. Hướng dẫn: https://code.claude.com/docs/en/cloud-environments#network-access

## Đợt xác minh qua tìm kiếm web (tạm dừng từ 01:52)
- Đã làm (01:50): lối ra 0,8 × 1,9 m → [TC]; bản thang F1.1 theo SĐ1:2023 (1,2 m khi > 15 người/tầng; 1,0 m khi ≤ 15) → [TC]; cách đo khoảng cách theo tim đường thoát nạn → [TC]; TCVN 13456:2022 (tên) → [TC]. Chưa tìm được: giá trị Bảng G.1, chiều rộng hành lang theo số người.
- 01:52: chạm giới hạn usage 5 giờ (reset 03:00 giờ VN = 20:00 UTC). **Đính chính 31/10:** KHÔNG có lịch tự chạy tiếp nào được tạo; phiên bị khởi động lại sau hạn chót 05:00 giờ VN nên đã dừng — việc còn lại làm ở phiên sau.
- Còn lại theo thứ tự: (1) xác minh tiếp: bậc chịu lửa Bảng 4, bộ phận ngăn cháy, đường xe 4,25 m, thang máy chữa cháy > 28 m, Phụ lục D (khói), TCVN 7336 Bảng 2 (diện tích/thời gian), TCVN 5738 (đầu báo), QCVN 10:2025 Phụ lục A, họng nước; (2) công cụ đọc bản vẽ (cắt ảnh PDF, đọc DXF), khởi tạo dự án; (3) CI GitHub Actions có tiền tố pccc; (4) tăng phiên bản 1.1.0, sync, doctor, push. Dừng hẳn trước 04:45 giờ VN.

## Việc tiếp theo (theo thứ tự ưu tiên)
1. (Chờ người dùng mở mạng) Truy cập thư mục Drive, liệt kê và tải các văn bản PCCC (QCVN 06:2022 + SĐ1:2023, QCVN 10:2025/BCA, TCVN 7336:2021, TCVN 5738:2021, TCVN 5687:2024, TCVN 3890:2023, QCVN 13:2018, NĐ 105/2025…).
2. Trích văn bản (pdftotext / đọc trang PDF), đối chiếu từng số liệu `[DC]` trong `pccc/knowledge/*.md` và `pccc/tools/du_lieu_tham_chieu.json`.
3. Sửa giá trị sai, nâng nhãn `[BG]` kèm trích dẫn (văn bản, mục, trang); cập nhật test nếu số liệu đổi.
4. Tăng phiên bản (VERSION + manifest), chạy `pccc_merge.py sync`, `pccc_doctor.py --tests`, commit & push sau mỗi văn bản.

## Cách tiếp tục ở phiên mới
1. `git pull` nhánh `ccr-dbc199ae-iq9ypg`.
2. Đọc file này + `pccc/memory/lich-su-lam-viec.md`.
3. Chạy `python3 pccc/integration/pccc_doctor.py --tests` để chắc trạng thái sạch.
4. Làm tiếp mục “Việc tiếp theo”.
