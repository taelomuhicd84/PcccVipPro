---
name: pccc-bao-chay
description: Thiết kế hệ thống báo cháy tự động, loa thông báo, liên động (ma trận nhân–quả), chiếu sáng sự cố, đèn chỉ dẫn thoát nạn, cấp điện ưu tiên và cáp chống cháy cho thiết bị PCCC theo QCVN 10:2025/BCA, TCVN 5738:2021, QCVN 06:2022; so sánh phương án hệ thường/địa chỉ/hỗn hợp, đèn tích hợp/ắc quy trung tâm. Dùng khi hỏi về báo cháy, đầu báo, chiếu sáng sự cố, điện cho PCCC (bao chay, den su co).
---

# /pccc-bao-chay — Báo cháy, liên động, chiếu sáng sự cố & điện PCCC

Tri thức: `pccc/knowledge/08-bao-chay.md`, `09-chieu-sang-su-co-dien.md`.

## Quy trình
1. **Diện phải trang bị**: báo cháy tự động & loa thông báo theo **QCVN 10:2025/BCA** (đã thu hẹp) — ghi rõ bắt buộc hay tự nguyện.
2. **Chọn đầu báo theo từng loại phòng** (khói/nhiệt/beam/ASD/lửa) — bảng phòng → loại đầu báo → lý do.
3. **Bố trí**: diện tích bảo vệ & khoảng cách theo chiều cao trần (`08` §2 [DC] — đối chiếu TCVN 5738:2021), xử lý dầm/ô trần; nút ấn, chuông/còi/đèn chớp; số kênh/loop.
4. **Trung tâm & nguồn**: vị trí phòng trực, nguồn dự phòng (tính dung lượng ắc quy theo dòng thường trực & báo động — ghi giả định).
5. **Liên động**: lập ma trận nhân – quả (`08` §4) đồng bộ với `pccc-hut-khoi` (thứ tự quạt), `pccc-thuy-luc` (bơm, công tắc dòng chảy), thang máy, cửa từ, màn ngăn cháy.
6. **Chiếu sáng sự cố & chỉ dẫn**: vị trí theo đường thoát nạn từ `pccc-thoat-nan`; độ rọi & thời gian theo tiêu chuẩn [DC].
7. **Cấp điện PCCC**: danh sách phụ tải ưu tiên, nguồn 2, ATS, tủ PCCC lấy trước aptomat tổng, cáp chống cháy, công suất máy phát (dòng khởi động bơm lớn nhất).
8. **Phương án** (≥ 2): thường ↔ địa chỉ ↔ hỗn hợp; ASD cho khu đặc biệt; đèn tích hợp ↔ ắc quy trung tâm ↔ hệ tự kiểm tra; diesel ↔ máy phát cho bơm.

## Đầu ra
Bảng thiết bị theo phòng, sơ đồ nguyên lý dạng mô tả (loop/kênh), ma trận nhân–quả, danh sách phụ tải PCCC & nguồn, so sánh phương án + khuyến nghị.
