# BÁO CÁO PHƯƠNG ÁN PCCC — <Tên công trình>

Mã dự án: `<mã>` · Giai đoạn: <…> · Ngày: <YYYY-MM-DD> · Người lập: <…> (hỗ trợ bởi Claude — module PCCC v<…>)
Căn cứ chính: QCVN 06:2022/BXD + SĐ1:2023; QCVN 10:2025/BCA; TCVN 7336:2021; TCVN 5738:2021; TCVN 5687; <…>
Quy ước: ✅ Đạt · ❌ Không đạt · 🔶 Đạt có điều kiện · ⚠️ Thiếu dữ liệu/cần đối chiếu · nhãn căn cứ `[BG] [TC] [DC] [QT]`.

## 0. Tóm tắt điều hành
| Hạng mục | Trạng thái | Phương án khuyến nghị | Chi phí tương đối | Rủi ro thẩm định |
|---|---|---|---|---|
| Thoát nạn | ❌ | PA-B: thang ngoài nhà loại 3 tại đầu hồi | Trung bình | Thấp |
| Ngăn cháy | ✅ | — | — | — |
| Cấp nước & sprinkler | thiết kế mới | PA-B: ống chính nhánh DN80, bơm 18,5 kW | — | Thấp |
| Chống khói | thiết kế mới | PA-A: 1 trục hút khói tập trung + N2 biến tần | — | Trung bình |
| … | | | | |

## 1. Thông tin công trình & bản vẽ đã dùng
Bảng tầng (cao độ, diện tích, công năng, số người) — trích `du-lieu-cong-trinh.json`. Danh mục bản vẽ.

## 2. Phân loại
Phiếu phân loại (`pccc/knowledge/02-phan-loai.md` §9) + bảng hệ thống bắt buộc (QCVN 10:2025/BCA).

## 3. Thoát nạn
### 3.1 Bảng kiểm tra
| # | Yêu cầu | Thiết kế | Đánh giá | Căn cứ |
|---|---|---|---|---|
### 3.2 Khoảng cách thoát nạn (đầu ra công cụ)
Lệnh: `python3 pccc/tools/thoat_nan.py duong-di --config pccc/du-an/<mã>/tinh-toan/duong-di-<tầng>.json`
<dán bảng>
### 3.3 Phương án
**Vấn đề:** <…>
| Tiêu chí | PA-A | PA-B | PA-C |
|---|---|---|---|
| Mô tả | | | |
| Điều khoản cho phép | | | |
| Đáp ứng quy chuẩn | | | |
| Chi phí đầu tư | | | |
| Chi phí vận hành | | | |
| Diện tích/không gian mất | | | |
| Thi công | | | |
| Rủi ro thẩm định | | | |
**Khuyến nghị:** PA-… vì …

## 4. Ngăn cháy & chống cháy lan
Bảng giới hạn chịu lửa cấu kiện · bảng khoang cháy · lỗ mở & xuyên khoang · mặt dựng · khoảng cách PCCC · phương án.

## 5. Tiếp cận chữa cháy
Đường/bãi xe, ô cửa tiếp cận, thang máy chữa cháy, họng tiếp nước · phương án.

## 6. Cấp nước chữa cháy & thủy lực
6.1 Thông số thiết kế (nhóm, cường độ, diện tích, Q, t) · 6.2 Sprinkler khu bất lợi (lệnh + bảng) · 6.3 Họng nước (lệnh + bảng, tầng cần giảm áp) · 6.4 Bể · 6.5 Bơm · 6.6 So sánh phương án & khuyến nghị.

## 7. Bảo vệ chống khói
7.1 Nơi phải hút khói/tăng áp · 7.2 Lưu lượng (lệnh + bảng) · 7.3 Bố trí trục, quạt, van, miệng gió (theo trục lưới/tầng) · 7.4 Liên động · 7.5 Phương án & khuyến nghị.

## 8. Báo cháy, liên động, chiếu sáng sự cố & điện PCCC
Thiết bị theo phòng · ma trận nhân – quả · phụ tải PCCC & nguồn · phương án.

## 9. Chữa cháy đặc biệt & phương tiện ban đầu
Khu đặc biệt → giải pháp · bình chữa cháy · phương án.

## 10. Giả định
| Mã | Nội dung | Ảnh hưởng nếu sai | Cần xác nhận bởi |
|---|---|---|---|

## 11. Câu hỏi cho chủ đầu tư / kiến trúc / kết cấu

## 12. Số liệu cần đối chiếu bản gốc ([DC])

## 13. Phụ lục tính toán
Danh sách file cấu hình `pccc/du-an/<mã>/tinh-toan/*.json` và lệnh để chạy lại.

---
*Báo cáo là tài liệu hỗ trợ kỹ thuật. Hồ sơ thiết kế phải được người có chứng chỉ hành nghề phù hợp kiểm tra, ký và cơ quan có thẩm quyền thẩm định theo quy định (Luật 55/2024/QH15, NĐ 105/2025/NĐ-CP).*
