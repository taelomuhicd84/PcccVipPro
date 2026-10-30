---
name: pccc-cap-nhat-tri-thuc
description: Cập nhật kho tri thức PCCC từ bản gốc văn bản (QCVN, TCVN, nghị định, thông tư) người dùng cung cấp hoặc khi phát hiện văn bản mới — trích điều khoản, sửa số liệu, nâng nhãn [DC]/[TC] lên [BG], đồng bộ du_lieu_tham_chieu.json, ghi nhật ký thay đổi. Dùng khi người dùng gửi file quy chuẩn/tiêu chuẩn, báo có văn bản mới, hoặc yêu cầu rà soát tri thức (cap nhat tri thuc).
---

# /pccc-cap-nhat-tri-thuc — Đối chiếu bản gốc & cập nhật tri thức

## Quy trình
1. **Nhận bản gốc**: lưu vào `pccc/knowledge/nguon/` theo quy ước tên trong `pccc/knowledge/nguon/README.md`. Ghi: số hiệu, ngày ban hành, ngày hiệu lực, văn bản thay thế.
2. **Trích nội dung**: PDF có chữ → `pdftotext -layout <file> -` (hoặc Read theo `pages`); PDF scan → đọc như ảnh. Ghi trang/ mục/ bảng cho từng số liệu.
3. **Đối chiếu**: tìm mọi số liệu liên quan trong `pccc/knowledge/*.md` và `pccc/tools/du_lieu_tham_chieu.json` (`grep -n "\[DC\]\|\[TC\]" pccc/knowledge/*.md`).
   - Khớp → đổi nhãn thành `[BG]` + thêm “(văn bản, mục…, tr.…)”.
   - Khác → sửa giá trị, nhãn `[BG]`, ghi giá trị cũ vào nhật ký.
   - JSON: đổi `"xm"` thành `"BG"`, cập nhật `"v"` và `"nguon"`.
4. **Văn bản mới/thay thế**: cập nhật `pccc/knowledge/01-van-ban-phap-ly.md` (bảng + §6 nhật ký), đổi `phien_ban_tri_thuc` trong `pccc/config.json`.
5. **Kiểm tra**: `python3 -m unittest discover -s pccc/tests` (test có thể khóa giá trị preset — cập nhật test nếu số liệu đổi có căn cứ) và `python3 pccc/integration/pccc_doctor.py`.
6. **Ghi nhớ**: thêm mục vào `pccc/memory/quyet-dinh.md` (văn bản, thay đổi, ảnh hưởng tới dự án đang làm).

## Nguyên tắc
- Không nâng nhãn khi chưa thấy bản gốc. Nguồn thứ cấp đáng tin chỉ được `[TC]`.
- Không xóa lịch sử: giá trị cũ ghi vào nhật ký với ngày.
- Thông báo cho người dùng các dự án trong `pccc/du-an/` có thể bị ảnh hưởng bởi thay đổi.
