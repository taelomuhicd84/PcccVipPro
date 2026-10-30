# Đơn giá tham khảo để so sánh phương án

Cập nhật: 2026-10-30

> ⚠️ Mọi đơn giá trong `pccc/tools/don_gia_mac_dinh.json` là **GIẢ ĐỊNH** chỉ để xếp hạng **tương đối** các phương án. Không dùng làm dự toán, không đưa vào hồ sơ như số liệu thật.

## 1. Cách dùng
1. Sao chép `pccc/tools/don_gia_mac_dinh.json` thành file của dự án, VD `pccc/du-an/<mã>/don-gia.json`, cập nhật theo báo giá thực tế (nhà thầu, nhà cung cấp, thời điểm, địa phương).
2. Chạy công cụ với `--don-gia pccc/du-an/<mã>/don-gia.json`.
3. Trong báo cáo ghi rõ nguồn đơn giá và ngày báo giá.

## 2. Mô hình chi phí trong công cụ
| Thành phần | Cách tính |
|---|---|
| Ống | Σ (chiều dài theo DN × đơn giá lắp đặt/m) — khai báo `khoi_luong_ong_m` cho từng phương án |
| Đầu phun | số đầu toàn hệ × đơn giá (`so_dau_toan_he`) |
| Bơm | 2 tổ (chính + dự phòng) × kW tiêu chuẩn × đơn giá/kW |
| Bể | thể tích × đơn giá/m³ |
| Điện năng vòng đời | kW × giờ chạy thử/năm × giá điện × số năm |
| Quạt (khói/tăng áp) | kW × đơn giá/kW × số quạt |
| Ống gió, bọc chống cháy, van | m² × đơn giá; số van × đơn giá |
| Kiểm soát áp (tăng áp) | van xả áp (m²) hoặc biến tần (kW) + cảm biến |

## 3. Tiêu chí so sánh ngoài chi phí (ghi trong báo cáo)
- Mức đáp ứng quy chuẩn & rủi ro thẩm định (ưu tiên giải pháp “theo quy chuẩn” hơn “giải pháp thay thế”).
- Ảnh hưởng kiến trúc (diện tích mất, mặt đứng, chiều cao thông thủy), kết cấu (tải trọng bể, quạt), tiến độ.
- Vận hành – bảo trì (số thiết bị, độ phức tạp điều khiển, phụ tùng).
- Độ tin cậy & dự phòng.
