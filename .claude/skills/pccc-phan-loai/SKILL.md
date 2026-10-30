---
name: pccc-phan-loai
description: Phân loại công trình theo QCVN 06:2022/BXD + SĐ1:2023 (chiều cao PCCC, bậc chịu lửa, cấp nguy hiểm cháy kết cấu S, nhóm nguy hiểm cháy theo công năng F1–F5, hạng nguy hiểm cháy nổ A–E, nhóm nguy cơ sprinkler) và lập danh mục hệ thống PCCC bắt buộc theo QCVN 10:2025/BCA. Dùng khi cần xác định công trình thuộc loại gì, phải trang bị hệ thống nào, có thuộc diện thẩm định thiết kế PCCC không.
---

# /pccc-phan-loai — Phân loại & danh mục hệ thống bắt buộc

Tri thức: `pccc/knowledge/02-phan-loai.md`, `01-van-ban-phap-ly.md`, `11-cong-trinh-dac-thu.md`.

## Các bước
1. **Công năng**: gán nhóm F cho từng phần (khối đế, tháp, hầm, gara). Nhà hỗn hợp → liệt kê từng phần + yêu cầu ngăn cách (chuyển sang `pccc-ngan-chay`). Áp dụng theo **công năng thực tế** (SĐ1:2023 mục 1.5.6) [TC].
2. **Chiều cao PCCC**: tính từ cao độ mặt đường xe chữa cháy thấp nhất tới mép dưới lỗ mở tầng trên cùng (không kể tầng kỹ thuật trên cùng) — trình bày phép tính. Thiếu dữ liệu → GĐ-xx.
3. **Bậc chịu lửa yêu cầu**: từ Phụ lục H (chiều cao + diện tích khoang cháy theo F, S); so với **bậc chịu lửa thực tế** (Bảng 4: giới hạn chịu lửa từng cấu kiện).
4. **Cấp S**: theo vật liệu kết cấu, bao che, mái.
5. **Hạng nguy hiểm cháy nổ** (F5 và gian phòng sản xuất/kho trong nhà khác): Phụ lục C; thiếu danh mục hàng hóa → hỏi chủ đầu tư.
6. **Nhóm nguy cơ sprinkler**: TCVN 7336:2021 Phụ lục A (`python3 pccc/tools/thuy_luc.py nhom` để xem thông số kèm nhãn).
7. **Hệ thống bắt buộc**: tra **QCVN 10:2025/BCA** (báo cháy, chữa cháy tự động, họng nước, bình, loa thông báo, phương tiện cứu nạn…) → đối chiếu TCVN 3890:2023 cho chi tiết kỹ thuật; hệ thống chống khói theo QCVN 06 Phụ lục D; thang máy chữa cháy, đường xe theo QCVN 06 Chương 6.
8. **Thủ tục**: thuộc diện thẩm định thiết kế về PCCC? (NĐ 105/2025/NĐ-CP, CV 5269/BXD-KTQLXD) [TC/DC].

## Đầu ra
- “Phiếu phân loại” (mẫu ở `02-phan-loai.md` §9) — mỗi dòng có căn cứ + nhãn.
- Bảng hệ thống: | Hệ thống | Bắt buộc? | Căn cứ | Ghi chú/đề xuất tự nguyện |.
- Danh sách giả định & câu hỏi.

## Lưu ý
- Phân loại sai kéo theo sai toàn bộ — nếu không chắc giữa hai phương án phân loại, trình bày cả hai và hệ quả của mỗi cách (đây cũng là “nhiều phương án”).
- Với yêu cầu “có phải trang bị X không”: luôn kiểm tra QCVN 10:2025/BCA trước (đã giảm diện so với TCVN 3890:2023).
