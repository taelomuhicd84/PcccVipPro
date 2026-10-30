---
name: pccc-thuy-luc
description: Thiết kế & tính toán thủy lực chữa cháy — họng nước chữa cháy trong nhà, sprinkler/drencher (TCVN 7336:2021), bể nước, trạm bơm, phân vùng áp lực; chạy công cụ thuy_luc.py để so sánh nhiều phương án (cỡ ống, K-factor, mạng vòng, cấu hình bơm, nguồn nước) và chọn phương án tối ưu tiết kiệm. Dùng khi hỏi về tính toán thủy lực, sprinkler, họng nước, bơm chữa cháy, bể nước chữa cháy (thuy luc, hong nuoc, bom chua chay).
---

# /pccc-thuy-luc — Cấp nước chữa cháy & thủy lực

Tri thức: `pccc/knowledge/05-cap-nuoc-chua-chay.md`, `06-chua-chay-tu-dong.md`, `13-don-gia-tham-khao.md`. Công cụ: `pccc/tools/thuy_luc.py` (xem `--help`, ví dụ trong `pccc/templates/vi-du/`).

## Quy trình
1. **Xác định hệ thống phải có** (từ `pccc-phan-loai`): họng nước trong nhà (số tia × l/s — tra QCVN 10:2025/BCA / TCVN 3890:2023 Bảng B.1), sprinkler (nhóm nguy cơ — `thuy_luc.py nhom`), drencher, ngoài nhà.
2. **Sprinkler — khu vực tính toán bất lợi nhất** (xa nhất/cao nhất so với trạm bơm):
   - Tạo `pccc/du-an/<mã>/tinh-toan/sprinkler.json` từ mẫu `pccc/templates/vi-du/sprinkler-gara.json`: nhóm, K, áp lực min, lưới đầu phun, cỡ ống nhánh/ống chính nhánh/ống cấp (chiều dài tương đương), chênh cao, tổn thất cụm van.
   - Chạy `python3 pccc/tools/thuy_luc.py sprinkler --config <file>`; đọc bảng áp lực từng đầu, K nhánh, Q, P bơm, thể tích nước, cảnh báo (vận tốc, áp lực làm việc).
3. **Họng nước**: `thuy_luc.py hong-nuoc --config <file>` (mẫu `hong-nuoc-chung-cu.json`): áp lực cần tại họng (lăng/vòi), tổn thất trục đứng, áp bơm, **danh sách tầng cần giảm áp**.
4. **Bể**: `thuy_luc.py be-nuoc --config <file>` — cộng các thành phần Q×t (ghi nhãn thời gian), kích thước gợi ý, số ngăn.
5. **Bơm**: `thuy_luc.py bom --q-l-s <Q> --h-m <H>` — kW động cơ, bơm bù áp, so sánh cấu hình B1/B2/B3.
6. **Phương án** (bắt buộc ≥ 2, thường 3) — thêm khóa `phuong_an` vào file cấu hình, mỗi PA ghi đè thông số + `khoi_luong_ong_m`, `so_dau_toan_he` để công cụ tính chi phí vòng đời và đề xuất:
   - cỡ ống ↔ cột áp bơm; K80 ↔ K115; lưới đầu phun; mạng nhánh ↔ mạng vòng;
   - hệ riêng ↔ hệ kết hợp; 1 vùng + van giảm áp ↔ nhiều vùng ↔ bơm trung chuyển;
   - nguồn nước: bể ngầm riêng / bể chung / bể thép / bể mái / nước đô thị (`05` §6.1).
7. **Kết luận tối ưu**: lấy đề xuất của công cụ (chi phí thấp nhất trong PA đạt) rồi xét tiêu chí ngoài chi phí (không gian phòng bơm, tải bể lên kết cấu, ồn, bảo trì, rủi ro thẩm định) → khuyến nghị cuối.

## Đầu ra
- Bảng thông số thiết kế (nhóm, cường độ, diện tích, Q, t, V) kèm căn cứ & nhãn.
- Bảng tính thủy lực (dán đầu ra công cụ) + lệnh đã chạy + file cấu hình lưu trong dự án.
- Bảng so sánh phương án + khuyến nghị + thông số chọn thiết bị (bơm Q-H-kW, bể V, cỡ ống chính).
- Cảnh báo: đơn giá giả định → cập nhật `--don-gia` theo báo giá thực tế.

## Lưu ý kỹ thuật
- Dùng đúng bảng đường kính trong (`bang_ong`: `sch40` hoặc `bs1387_m`) theo ống thực tế.
- Hệ khô/tiền kích hoạt: C = 100. Ống nhựa/inox: C = 150.
- Lưu lượng thiết kế cho bơm/bể = max(tính toán, lưu lượng tối thiểu của nhóm); thời gian theo TCVN 7336 [DC].
- Áp lực tĩnh lớn nhất trong mạng ≤ áp định mức thiết bị (thường PN16) — nếu vượt phải phân vùng.
