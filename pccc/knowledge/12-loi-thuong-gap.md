# Lỗi hay gặp khi thẩm định thiết kế PCCC — và cách khắc phục

Cập nhật: 2026-10-30 · Nguồn: kinh nghiệm thực hành chung [QT]; bổ sung lỗi thực tế từ dự án vào `pccc/memory/bai-hoc.md`.

| # | Lỗi | Hậu quả | Cách khắc phục / phương án | Skill |
|---|---|---|---|---|
| 1 | Lấy chiều cao kiến trúc thay cho **chiều cao PCCC** | Sai loại buồng thang, thang máy chữa cháy, hệ thống bắt buộc | Tính lại từ mặt đường xe chữa cháy thấp nhất tới mép dưới cửa sổ tầng trên cùng | `pccc-phan-loai` |
| 2 | Bỏ sót tầng kỹ thuật, tum, tầng lửng khi tính số tầng/diện tích | Sai khoang cháy, sai số lối ra | Lập bảng tầng đầy đủ từ mặt cắt | `pccc-doc-ban-ve` |
| 3 | Thang hầm thông thẳng với thang tầng nổi | Khói từ hầm lan lên buồng thang | Tách thang/ngăn cháy tại tầng 1 + lối ra riêng; sảnh ngăn khói tầng hầm (SĐ1:2023) | `pccc-thoat-nan` |
| 4 | Cửa buồng thang mở ngược chiều thoát nạn, không tự đóng, không đạt EI | Không đạt điều kiện buồng thang | Đổi chiều mở, bổ sung tay co thủy lực, cửa có chứng nhận | `pccc-thoat-nan` |
| 5 | Hành lang cụt vượt giới hạn do căn góc/ căn cuối hành lang | Không đạt khoảng cách thoát nạn | Thêm thang/ thang ngoài loại 3/ tổ chức lại mặt bằng (`03-thoat-nan.md` §4.1) | `pccc-thoat-nan` |
| 6 | Không có lối ra khẩn cấp cho căn hộ ở cao khi tầng chỉ 1 lối ra | Không đạt | Ban công/lô gia đạt điều kiện hoặc bổ sung lối ra thứ 2 | `pccc-thoat-nan` |
| 7 | Ống gió xuyên tường/sàn ngăn cháy không có van ngăn cháy; trục kỹ thuật không chèn sàn | Cháy lan qua khoang | Van ngăn cháy + chèn bịt; bọc ống chịu lửa | `pccc-ngan-chay` |
| 8 | Atrium/thông tầng không tính khoang cháy gộp | Vượt diện tích khoang cháy | Màn/kính ngăn cháy hoặc tính gộp + sprinkler + hút khói | `pccc-ngan-chay` |
| 9 | Miệng hút khói đặt thấp/ quá xa; quạt không đạt nhiệt độ; thiếu cấp bù | Hút khói không hiệu quả | Bố trí lại theo `07-chong-khoi.md` §4; tính lại bằng `hut_khoi.py` | `pccc-hut-khoi` |
| 10 | Tăng áp không kiểm soát quá áp → cửa không mở nổi | Nguy hiểm thoát nạn | Van xả áp/biến tần; kiểm tra lực mở cửa | `pccc-hut-khoi` |
| 11 | Miệng lấy gió tăng áp gần miệng xả khói | Thổi khói vào buồng thang | Dời miệng lấy gió (tầng thấp/ hướng khác, cách xa) | `pccc-hut-khoi` |
| 12 | Bể chung sinh hoạt không giữ được dự trữ chữa cháy | Thiếu nước khi cháy | Ống hút sinh hoạt đặt cao, báo mực nước; hoặc bể riêng | `pccc-thuy-luc` |
| 13 | Bơm dự phòng nhỏ hơn bơm chính; nguồn điện không ưu tiên | Không đạt độ tin cậy | Bơm dự phòng cùng thông số; 2 nguồn/diesel; cáp chống cháy | `pccc-thuy-luc` |
| 14 | Sai nhóm nguy cơ sprinkler (VD gara lấy nhóm 1) | Thiếu lưu lượng, bể nhỏ | Tra TCVN 7336:2021 Phụ lục A; tính lại | `pccc-thuy-luc` |
| 15 | Đầu phun bị dầm/ống gió che chắn; khoảng cách vượt | Vùng không được bảo vệ | Bổ sung đầu phun dưới vật cản; chỉnh lưới | `pccc-thuy-luc` |
| 16 | Cáp nguồn PCCC là cáp thường, đi chung máng | Mất nguồn khi cháy | Cáp chống cháy, tuyến riêng, tủ PCCC lấy trước aptomat tổng | `pccc-bao-chay` |
| 17 | Đường xe chữa cháy bị cây xanh, mái che, cổng thấp cản trở; mái hầm không đủ tải | Xe không tiếp cận | Điều chỉnh tổng mặt bằng/ gia cường | `pccc-tiep-can-chua-chay` |
| 18 | Không thể hiện giới hạn chịu lửa kết cấu (lớp bảo vệ cốt thép, sơn chống cháy kết cấu thép) | Thiếu hồ sơ bậc chịu lửa | Bảng giới hạn chịu lửa từng cấu kiện, chứng nhận vật liệu | `pccc-ngan-chay` |
| 19 | Vật liệu ốp mặt dựng/ hoàn thiện đường thoát nạn không đạt | Cháy lan, khói độc | Đổi vật liệu đạt nhóm yêu cầu | `pccc-ngan-chay` |
| 20 | Áp dụng TCVN 3890 cũ thay vì **QCVN 10:2025/BCA** cho diện trang bị | Thừa/thiếu hệ thống | Tra lại theo QCVN 10:2025/BCA (từ 30/12/2025) | `pccc-phan-loai` |
| 21 | Thuyết minh không dẫn điều khoản; số liệu bản vẽ ≠ thuyết minh | Bị yêu cầu giải trình | Dùng mẫu báo cáo `pccc/templates/bao-cao-phuong-an.md`; đối chiếu chéo | `pccc-bao-cao` |
