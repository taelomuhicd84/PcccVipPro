---
name: pccc-doc-ban-ve
description: Đọc bản vẽ kiến trúc/MEP (ảnh, PDF, xuất từ CAD) để trích xuất dữ liệu phục vụ PCCC — số tầng, chiều cao, diện tích, công năng, số người, thang bộ, hành lang, cửa, khoảng cách thoát nạn, kết cấu, đường xe chữa cháy — vào phiếu dữ liệu công trình JSON và lập danh sách thông tin còn thiếu. Dùng ở bước đầu mỗi khi nhận bản vẽ (doc ban ve, mat bang, mat cat).
---

# /pccc-doc-ban-ve — Đọc bản vẽ → dữ liệu công trình

## 1. Mở bản vẽ
- Ảnh: đọc trực tiếp (Read). PDF: Read với tham số `pages` (≤ 20 trang/lần); lấy chữ & kích thước: `pdftotext -layout file.pdf -` (nếu có), thông tin trang: `pdfinfo`.
- PDF scan/ảnh mờ: đọc như ảnh; ghi rõ chỗ không đọc được.
- DWG: đề nghị người dùng xuất PDF/PNG theo từng tầng (hoặc DXF). Không đoán nội dung không thấy.
- Lưu bản gốc vào `pccc/du-an/<mã>/input/` (tên ASCII, VD `MB-tang-1.pdf`).

## 2. Thứ tự đọc
1. **Tổng mặt bằng**: lối vào, đường nội bộ (bề rộng, bán kính quay, đường cụt), cổng & mái che (chiều cao), nhà lân cận (khoảng cách), trụ nước, cao độ mặt đường.
2. **Mặt cắt**: cao độ từng sàn, chiều cao tầng, tầng kỹ thuật/tum, cao độ mép dưới cửa sổ tầng trên cùng → tính **chiều cao PCCC**.
3. **Mặt bằng từng tầng**: công năng từng khu, diện tích, số người/ số chỗ, vị trí & loại thang bộ, thang máy, hành lang (bề rộng), cửa (rộng, chiều mở), lối ra ngoài, phòng kỹ thuật, trục kỹ thuật, thông tầng.
4. **Mặt đứng**: cửa sổ, ban công/lô gia, vật liệu mặt dựng, băng tường đặc giữa các tầng.
5. **Kết cấu/ thuyết minh**: loại kết cấu, vật liệu, lớp bảo vệ → bậc chịu lửa, cấp S.
6. **MEP (nếu có)**: trục ống, phòng bơm, bể, quạt, phòng điện, máy phát.

## 3. Ghi dữ liệu
- Điền `pccc/du-an/<mã>/du-lieu-cong-trinh.json` theo mẫu `pccc/templates/du-lieu-cong-trinh.json`.
- Mỗi giá trị ghi `nguon`: tên bản vẽ + vị trí (VD “MB-tang-3, trục C-D”) hoặc `GĐ-xx` nếu là giả định.
- Khoảng cách thoát nạn: lập đồ thị nút/cạnh theo tim hành lang (tọa độ m) cho `pccc/tools/thoat_nan.py duong-di` (mẫu `pccc/templates/vi-du/duong-di-tang-dien-hinh.json`).
- Ưu tiên kích thước ghi trên bản vẽ; đo theo tỷ lệ thì ghi “đo tỷ lệ 1/…, ±…”.

## 4. Đầu ra
1. File JSON dữ liệu công trình.
2. Bảng tóm tắt (tầng | cao độ | diện tích | công năng | số người | thang | ghi chú).
3. **Danh sách thiếu/ mâu thuẫn** (VD diện tích ghi trên bản vẽ ≠ đo; số tầng mặt cắt ≠ mặt bằng) và câu hỏi cho người dùng.

## Bẫy hay gặp
- Nhầm cao độ ±0.000 (sàn tầng 1) với cao độ mặt đường xe chữa cháy.
- Bỏ sót tầng lửng, tầng kỹ thuật, tum thang, mái tầng hầm làm sân.
- Cửa vẽ tượng trưng sai chiều mở; cửa cuốn/ cửa trượt bị coi như lối ra thoát nạn.
- Hành lang bị thu hẹp bởi cột, hộp kỹ thuật, tủ chữa cháy.
