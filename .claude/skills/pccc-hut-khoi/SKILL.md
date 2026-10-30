---
name: pccc-hut-khoi
description: Thiết kế bảo vệ chống khói theo QCVN 06:2022/BXD Phụ lục D + SĐ1:2023 — hút khói hành lang, gian phòng, tầng hầm/gara, atrium; cấp bù; tăng áp buồng thang N2, khoang đệm N3, giếng thang máy; tính lưu lượng bằng hut_khoi.py (TCVN 5687 Phụ lục L, NFPA 92, EN 12101-6), chọn tuyến ống gió, vị trí quạt, miệng hút/miệng cấp, kiểm soát quá áp và so sánh phương án. Dùng khi hỏi về hút khói, tăng áp, quạt, ống gió PCCC (hut khoi, tang ap).
---

# /pccc-hut-khoi — Hút khói, cấp bù, tăng áp

Tri thức: `pccc/knowledge/07-chong-khoi.md` (yêu cầu §1–2, công thức §3, **bố trí ống/quạt/miệng gió §4**, phương án §5). Công cụ: `pccc/tools/hut_khoi.py`.

## Quy trình
1. **Xác định nơi phải hút khói / tăng áp** theo Phụ lục D (hành lang, phòng, hầm, atrium; buồng thang N2/N3, giếng thang, sảnh thang máy chữa cháy) — ghi căn cứ & nhãn; nêu chỗ được miễn (thông gió tự nhiên đủ điều kiện).
2. **Chia khoang khói** (hành lang theo chiều dài phục vụ 1 miệng; hầm/gara theo màn ngăn khói/dầm).
3. **Tính lưu lượng**:
   - Hành lang: `python3 pccc/tools/hut_khoi.py hanh-lang --config <file>` (B, H, n, Kd — tra Bảng L1 TCVN 5687; nhiệt độ khói; rò rỉ).
   - Gian phòng: `hut_khoi.py phong` (Pf, y, Ks; kiểm tra phạm vi L.2).
   - Sảnh lớn/atrium: chạy cả `phong` và `nfpa92` để đối chứng (mẫu `hut-khoi-atrium.json`).
   - Tăng áp: `hut_khoi.py tang-ap` (Δp 20–50 Pa, rò rỉ cửa, tiêu chí cửa mở, xả áp, lực mở cửa) — mẫu `tang-ap-buong-thang.json`.
4. **Chọn ống & quạt**: `hut_khoi.py ong-gio --q-m3-h <Q> --v-max <v> --t-c <t>` → kích thước; cộng tổn thất (ma sát × chiều dài + cục bộ) để chọn cột áp quạt; nhiệt độ làm việc của quạt hút khói theo quy định.
5. **Bố trí** (viết rõ trong báo cáo):
   - Trục đứng hút khói: vị trí theo trục lưới (VD “trục 5–6/C, sát hành lang”), kích thước, vật liệu, giới hạn chịu lửa.
   - Van hút khói mỗi tầng: cao độ lắp (dưới trần, trên mép cửa), loại (thường đóng), điều khiển.
   - Quạt: vị trí (mái/tầng kỹ thuật), phòng quạt hay ngoài trời, hướng xả, khoảng cách tới miệng lấy gió tăng áp/ cửa sổ.
   - Cấp bù: nguồn gió, vị trí miệng cấp (thấp), vận tốc.
   - Tăng áp: điểm lấy gió tươi (không bị khói), cấp 1 điểm hay nhiều điểm, cách kiểm soát quá áp.
   - Liên động: thứ tự khởi động (hút trước, cấp sau 20–30 s [DC]), dừng thông gió thường.
6. **Phương án** (≥ 2): 1 trục tập trung ↔ nhiều trục theo khoang; cơ khí ↔ tự nhiên; ống gió ↔ jet fan (gara); xả áp ↔ biến tần; cấp 1 điểm ↔ nhiều điểm — dùng `phuong_an` trong file cấu hình để công cụ so sánh chi phí (quạt, ống, bọc chống cháy, van, điều khiển).

## Đầu ra
- Bảng nơi phải hút khói/tăng áp + căn cứ.
- Bảng tính lưu lượng từng hệ (dán đầu ra công cụ + file cấu hình lưu tại `pccc/du-an/<mã>/tinh-toan/`).
- Mô tả tuyến ống, vị trí quạt & miệng gió theo trục/ tầng; danh mục thiết bị (quạt Q–Δp–kW–nhiệt độ; van; ống gió kích thước & EI).
- So sánh phương án + khuyến nghị.

## Bẫy hay gặp
Miệng hút đặt thấp/ quá xa; quạt không chịu nhiệt; thiếu cấp bù; miệng lấy gió tăng áp gần miệng xả khói; không kiểm soát quá áp → cửa buồng thang không mở nổi; dùng chung trục hút khói với thông gió thường không có biện pháp.
