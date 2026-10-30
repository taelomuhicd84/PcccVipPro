# Báo cháy tự động, thông báo & liên động

Cập nhật: 2026-10-30 · Căn cứ: QCVN 10:2025/BCA (diện phải trang bị — đã thu hẹp) [TC], TCVN 5738:2021 (yêu cầu kỹ thuật) [DC], TCVN 3890:2023 [TC], NFPA 72 [QT].

## 1. Khi nào phải có
- Báo cháy tự động: tra **QCVN 10:2025/BCA Phụ lục A** — số loại công trình bắt buộc đã giảm đáng kể so với TCVN 3890:2023 [TC].
- Hệ thống loa thông báo & hướng dẫn thoát nạn: QCVN 10:2025/BCA điều chỉnh (VD bỏ yêu cầu với nhà kho có tổng diện tích sàn ≥ 18 000 m² và ≥ 50 người/tầng) [TC]; các trường hợp còn lại tra bảng [DC].

## 2. Đầu báo cháy — bố trí tham khảo (TCVN 5738:2021) [DC]
| Loại | Chiều cao trần | Diện tích bảo vệ 1 đầu | Khoảng cách giữa đầu | Tới tường |
|---|---|---|---|---|
| Khói (điểm) | ≤ 3,5 m | ≤ 85 m² | ≤ 9,0 m | ≤ 4,5 m |
| Khói (điểm) | 3,5 – 6 m | ≤ 70 m² | ≤ 8,5 m | ≤ 4,0 m |
| Khói (điểm) | 6 – 10 m | ≤ 65 m² | ≤ 8,0 m | ≤ 4,0 m |
| Khói (điểm) | 10 – 12 m | ≤ 55 m² | ≤ 7,5 m | ≤ 3,5 m |
| Nhiệt (điểm) | ≤ 3,5 m | ≤ 25 m² | ≤ 5,0 m | ≤ 2,5 m |
| Nhiệt (điểm) | 3,5 – 6 m | ≤ 20 m² | ≤ 4,5 m | ≤ 2,0 m |
| Nhiệt (điểm) | 6 – 9 m | ≤ 15 m² | ≤ 4,0 m | ≤ 2,0 m |

Quy tắc chung [DC]: mỗi gian phòng thường ≥ 2 đầu báo (hoặc điều kiện cho phép 1 đầu); trần có dầm sâu chia ô → xét từng ô; tránh đặt đầu khói gần miệng gió cấp; khu bếp, phòng máy phát, bãi xe có khói thải → đầu nhiệt; trần cao/sảnh lớn → đầu báo khói tia chiếu (beam) hoặc hút mẫu (ASD); kho xăng dầu → đầu báo lửa; phòng máy chủ → ASD/báo khói sớm.

## 3. Thiết bị khác [DC]
- Nút ấn báo cháy: tại lối ra, buồng thang, hành lang; độ cao lắp và khoảng cách giữa các nút theo TCVN 5738.
- Chuông/còi/đèn chớp: đủ mức âm thanh trên nền ồn (yêu cầu tối thiểu & vượt nền theo tiêu chuẩn); đèn chớp cho khu ồn/khu người khuyết tật nghe.
- Trung tâm báo cháy: tại phòng trực 24/24 (thường tầng 1, gần lối vào), có nguồn dự phòng ắc quy đủ thời gian thường trực + báo động theo tiêu chuẩn.
- Cáp: mạch tín hiệu & liên động quan trọng dùng cáp chống cháy/ đi trong ống bảo vệ (xem `09-chieu-sang-su-co-dien.md`).

## 4. Liên động (ma trận nhân – quả)
| Tín hiệu | Hành động |
|---|---|
| Báo cháy khu/tầng | Kích hoạt chuông/loa khu liên quan; mở van hút khói tầng cháy; chạy quạt hút khói → 20–30 s sau chạy cấp bù & tăng áp [DC] |
| Báo cháy bất kỳ | Dừng AHU/thông gió thường, đóng van ngăn cháy điện; thang máy về tầng 1 (trừ thang máy chữa cháy); mở khóa từ cửa thoát nạn; hạ cửa/màn ngăn cháy tự động |
| Công tắc dòng chảy sprinkler | Báo cháy theo khu; khởi động bơm (qua công tắc áp lực) |
| Xả khí | Đếm ngược, đèn “KHÍ ĐANG XẢ”, ngắt điều hòa phòng, đóng van gió |
| Giám sát | Trạng thái bơm, quạt, van, nguồn, lỗi đường dây hiển thị tại trung tâm |

## 5. Thư viện phương án
| PA | Giải pháp | Phù hợp | Ghi chú |
|---|---|---|---|
| A | Hệ thường (conventional) theo kênh/khu | Công trình nhỏ, ít khu | Rẻ; khó định vị chính xác |
| B | Hệ địa chỉ (addressable) | Công trình vừa – lớn, nhiều liên động | Định vị từng thiết bị, dây vòng (loop) chịu đứt 1 điểm |
| C | Hệ hỗn hợp: địa chỉ cho khu chung + thường cho căn hộ/khu nhỏ | Chung cư, khách sạn | Tối ưu chi phí |
| D | Báo khói sớm hút mẫu (ASD) cho khu đặc biệt | Phòng máy chủ, kho cao, atrium | Phát hiện sớm, chi phí cao |
| E | Không dây (wireless) bổ sung | Cải tạo công trình cũ, di tích | Pin phải giám sát; chứng nhận phù hợp |
