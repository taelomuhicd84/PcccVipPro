---
name: pccc-thoat-nan
description: Kiểm tra lối thoát nạn theo QCVN 06:2022/BXD + SĐ1:2023 (số lối ra, bố trí phân tán, chiều rộng cửa/hành lang/bản thang, khoảng cách thoát nạn, hành lang cụt, loại buồng thang L1/L2/N1/N2/N3, thang hầm, lối ra khẩn cấp) và đề xuất nhiều phương án khắc phục khi không đạt. Dùng khi hỏi về thoát nạn, thoát hiểm, cầu thang thoát hiểm, hành lang, cửa thoát nạn (thoat nan, thoat hiem).
---

# /pccc-thoat-nan — Kiểm tra & phương án thoát nạn

Tri thức: `pccc/knowledge/03-thoat-nan.md` (yêu cầu + thư viện phương án §4). Công cụ: `pccc/tools/thoat_nan.py`.

## Quy trình
1. **Chuẩn bị**: phiếu phân loại (nhóm F, chiều cao PCCC, bậc chịu lửa, cấp S) — chưa có thì chạy `pccc-phan-loai` trước.
2. **Số người**: `python3 pccc/tools/thoat_nan.py so-nguoi --config <file>` (ưu tiên số người theo nhiệm vụ thiết kế/ số chỗ).
3. **Số lối ra mỗi gian/tầng/tầng hầm** — đối chiếu điều kiện cho phép 1 lối ra.
4. **Phân tán**: `thoat_nan.py phan-tan` (L ≥ 1,5·√P [DC] + kiểm tra chéo đường chéo [QT]).
5. **Khoảng cách**: lập đồ thị hành lang (tọa độ m) → `thoat_nan.py duong-di --config <file>`; nhập `gioi_han` {giua, cut} tra từ Phụ lục G (ghi `nguon_gioi_han` + nhãn). Công cụ tự xác định cửa nằm “giữa các lối ra” hay “hành lang cụt”.
6. **Kích thước**: cửa, hành lang, bản thang, chiều cao thông thủy (dầm, ống gió, hạ trần) → `thoat_nan.py chieu-rong` cho tổng bề rộng theo số người.
7. **Buồng thang**: loại (L1/L2/N1/N2/N3) có phù hợp chiều cao PCCC; thang hầm tách thang nổi; sảnh ngăn khói tầng hầm (SĐ1:2023); lối ra trực tiếp ra ngoài ở tầng 1.
8. **Cửa**: chiều mở, loại cửa (không cửa cuốn/trượt/xoay), tự đóng, giới hạn chịu lửa, khóa.
9. **Lối ra khẩn cấp** cho căn hộ ở cao khi tầng chỉ có 1 lối ra.
10. **Phương án**: mỗi ❌ → ≥ 2 phương án từ thư viện §4 (có thể chạy `duong-di` với `phuong_an` dùng `loi_ra_them`, `canh_them` để chứng minh phương án đạt — ví dụ `pccc/templates/vi-du/duong-di-tang-dien-hinh.json`).

## Đầu ra
- Bảng kiểm tra (định dạng `pccc/MODULE.md` §4), từng tầng điển hình + tầng hầm + tầng 1.
- Bảng khoảng cách từ công cụ (dán nguyên bảng + lệnh đã chạy).
- Khối phương án & khuyến nghị; sơ đồ mô tả bằng lời vị trí thang/ lối ra mới (trục, tầng).
- Giả định & câu hỏi (VD số người hội trường, chiều cao PCCC).
