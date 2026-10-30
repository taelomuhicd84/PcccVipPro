# Chiếu sáng sự cố, chỉ dẫn thoát nạn & cấp điện cho PCCC

Cập nhật: 2026-10-30 · Căn cứ: QCVN 06:2022/BXD [DC], TCVN 13456:2022 (đèn sự cố & chỉ dẫn — kiểm tra số hiệu) [DC], QCVN 10:2025/BCA [TC — phạm vi], IEC 60331 / BS 6387 / BS 8491 (cáp chống cháy) [QT].

## 1. Chiếu sáng sự cố & đèn chỉ dẫn [DC]
- Bố trí trên mọi đường thoát nạn: hành lang, buồng thang, sảnh, lối ra, chỗ đổi hướng/đổi cao độ, gần thiết bị PCCC (tủ họng nước, nút ấn, bình), phòng bơm, phòng điều khiển, trạm biến áp, phòng máy phát.
- Độ rọi tối thiểu trên sàn đường thoát nạn và thời gian duy trì theo tiêu chuẩn (thường ≥ 1 lux; ≥ 1 h — nhà cao/đông người có thể yêu cầu cao hơn) — PHẢI tra bản gốc.
- Đèn “LỐI RA/EXIT” trên cửa lối ra thoát nạn; đèn chỉ hướng tại mọi chỗ không nhìn thấy trực tiếp lối ra; khoảng cách nhìn theo kích thước chữ.
- Nguồn: ắc quy tích hợp (self-contained) hoặc ắc quy trung tâm; tự chuyển khi mất điện; có chế độ tự kiểm tra là ưu điểm.

## 2. Cấp điện cho thiết bị PCCC [DC]
- Phụ tải PCCC (bơm chữa cháy, quạt tăng áp/hút khói, thang máy chữa cháy, chiếu sáng sự cố, báo cháy, cửa/màn ngăn cháy tự động, trung tâm điều khiển) thuộc **phụ tải ưu tiên**: 2 nguồn (lưới + máy phát/ nguồn độc lập), chuyển nguồn tự động (ATS).
- Tủ điện PCCC riêng, lấy nguồn **trước** aptomat tổng (không bị cắt khi cắt điện sinh hoạt lúc cháy); có biển “ĐIỆN PCCC — KHÔNG CẮT”.
- Cáp cấp nguồn & điều khiển PCCC: **cáp chống cháy** (duy trì mạch trong thời gian theo yêu cầu), đi tuyến riêng/ trong trục kỹ thuật được bảo vệ, không chung máng với cáp thường hoặc có vách ngăn.
- Máy phát: công suất đủ khởi động bơm chữa cháy lớn nhất + phụ tải PCCC đồng thời (tính dòng khởi động; cân nhắc khởi động sao–tam giác/ mềm).

## 3. Thư viện phương án
### 3.1 Chiếu sáng sự cố
| PA | Giải pháp | Ưu | Nhược |
|---|---|---|---|
| A | Đèn tích hợp ắc quy (self-contained) | Đơn giản, độc lập từng đèn | Thay ắc quy định kỳ, bảo trì phân tán |
| B | Hệ ắc quy trung tâm (central battery) | Bảo trì tập trung, giám sát | Cáp chống cháy tới từng đèn, phòng ắc quy |
| C | Hệ địa chỉ tự kiểm tra (addressable self-test) | Báo lỗi tự động, giảm nhân công kiểm tra | Chi phí cao |
### 3.2 Nguồn cho bơm chữa cháy
A: lưới + máy phát (ATS) · B: bơm diesel dự phòng (không phụ thuộc điện) · C: 2 tuyến lưới từ 2 trạm biến áp khác nhau (khi có) — so sánh tại `thuy_luc.py bom`.
