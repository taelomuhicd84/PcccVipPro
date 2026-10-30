# Cấp nước chữa cháy — họng nước, nguồn nước, trạm bơm, thủy lực

Cập nhật: 2026-10-30 · Căn cứ: QCVN 10:2025/BCA (trang bị — bắt buộc) [TC], TCVN 3890:2023 Bảng B.1 [TC], QCVN 06:2022/BXD (cấp nước chữa cháy) [DC], TCVN 2622:1995 / TCVN 4513:1988 / TCVN 13606:2023 [DC]. Công cụ: `pccc/tools/thuy_luc.py`.

## 1. Hệ thống họng nước chữa cháy trong nhà
- **Khi nào phải có**: tra QCVN 10:2025/BCA (bảng trang bị họng nước) → đối chiếu TCVN 3890:2023 Bảng B.1 [TC].
- **Số tia × lưu lượng mỗi tia**: tra bảng tương ứng theo loại nhà, số tầng/chiều cao, khối tích [DC]. Lưu lượng 1 tia phổ biến **2,5 l/s** [TC]. Một số trường hợp nhà cao (bản QCVN 06:2021, Phụ lục A): ≥ 4 tia × 2,5 l/s, thời gian ≥ 1 h, mỗi điểm sàn có 2 họng phun tới đồng thời [TC — từ bản 2021, kiểm tra bản 2022].
- **Bố trí** [DC]: mỗi điểm của gian phòng có số tia yêu cầu phun tới; họng đặt gần lối ra, sảnh, buồng thang (dễ tiếp cận, không bị khóa); tâm van ở độ cao khoảng 1,25 m; tủ gồm van góc, vòi (DN50, dài 20 m hoặc theo tính toán), lăng phun 13–16 mm.
- **Áp lực**: tại họng bất lợi phải đủ tạo chiều cao cột nước đặc yêu cầu [DC]; tại họng có áp lực quá lớn (thường > 0,4–0,45 MPa [DC]) phải có màng tiết lưu/van giảm áp. → `thuy_luc.py hong-nuoc` tự tính áp lực cần tại van từ lăng & vòi [VL] và liệt kê tầng cần giảm áp.
- **Mạng ống** [DC]: mạng vòng hoặc ≥ 2 đường cấp vào khi số họng lớn; van chặn phân đoạn để sửa chữa không mất quá số họng cho phép; trụ/họng tiếp nước cho xe chữa cháy (≥ 2 đầu nối DN65) đặt nơi xe tiếp cận được.

## 2. Cấp nước chữa cháy ngoài nhà [DC]
- Lưu lượng theo khối tích, bậc chịu lửa, hạng nguy hiểm, số đám cháy đồng thời (TCVN 2622 / TCVN 13606 / quy định áp dụng).
- Trụ nước chữa cháy: dọc đường giao thông, khoảng cách giữa các trụ & tới mép đường/tường nhà theo tiêu chuẩn; có thể lấy từ mạng đô thị (cần văn bản xác nhận lưu lượng, áp lực của đơn vị cấp nước) hoặc bể riêng + bơm.
- Thời gian chữa cháy ngoài nhà thường tính **3 giờ** [DC].

## 3. Nguồn nước & bể chữa cháy
- Dung tích: **V = Σ Qᵢ × tᵢ** (họng nước trong nhà, sprinkler/drencher, ngoài nhà nếu lấy từ bể) [VL] → `thuy_luc.py be-nuoc`.
- Thời gian tính toán: họng nước trong nhà **3 h** (thực hành theo TCVN 2622) [DC]; sprinkler theo TCVN 7336:2021 (thực hành: nhóm 1 – 30 phút, nhóm 2–3 – 60 phút) [DC].
- Được trừ lượng nước bổ sung trong khi chữa cháy **chỉ khi** nguồn cấp được bảo đảm (văn bản xác nhận) [DC].
- Bể dùng chung với sinh hoạt: phải có biện pháp bảo đảm dự trữ chữa cháy không bị dùng (ống hút sinh hoạt đặt cao hơn mực dự trữ, báo mực nước) [DC].
- Thời gian phục hồi lượng nước dự trữ chữa cháy (thường ≤ 24 h) [DC]; nên chia ≥ 2 ngăn để vệ sinh không mất toàn bộ dự trữ [QT].

## 4. Trạm bơm chữa cháy [DC trừ khi ghi khác]
- Bơm chính + **bơm dự phòng có lưu lượng, cột áp không nhỏ hơn bơm chính**; bơm bù áp duy trì áp lực mạng.
- Nguồn điện: 2 nguồn độc lập (lưới + máy phát) hoặc bơm diesel; cáp chống cháy từ tủ ưu tiên tới phòng bơm (`09-chieu-sang-su-co-dien.md`).
- Khởi động tự động (công tắc áp lực/dòng chảy) + bằng tay tại chỗ + từ phòng trực; không tự dừng khi đang chữa cháy.
- Phòng bơm: ngăn cháy với khu vực khác, lối ra trực tiếp ra ngoài hoặc vào buồng thang; chiếu sáng sự cố; thoát nước sàn; thông gió (bơm diesel cần khí đốt & ống xả).
- Đo kiểm: đồng hồ áp suất, đường ống thử lưu lượng hoặc đồng hồ lưu lượng để nghiệm thu/ bảo dưỡng.

## 5. Phương pháp tính thủy lực (dùng trong công cụ)
| Nội dung | Công thức / giả thiết | Nhãn |
|---|---|---|
| Tổn thất dọc đường | Hazen–Williams: p (bar/m) = 6,05·10⁵·Q^1,85 / (C^1,85·d^4,87), Q L/min, d mm (đường kính trong) | [VL] |
| Hệ số C | thép đen/mạ kẽm hệ ướt 120; hệ khô/tiền kích hoạt 100; nhựa/inox/đồng 150 | [QT] |
| Tổn thất cục bộ | hệ số phụ kiện 1,1–1,2 hoặc chiều dài tương đương | [QT] |
| Chênh cao | 1 m cột nước = 0,0981 bar | [VL] |
| Lưu lượng đầu phun | q = K·√p (K: L/min/bar^0,5) | [VL] |
| Vận tốc khuyến nghị | ống họng nước ≤ 3 m/s; ống sprinkler cảnh báo > 6 m/s | [QT] |
| Đường kính trong | Sch40 (ASME) hoặc BS 1387 Medium — chọn đúng bảng ống thực tế | [VL] |

## 6. Thư viện phương án (dùng `thuy_luc.py` để lượng hóa)

### 6.1 Nguồn nước
| PA | Giải pháp | Ưu | Nhược |
|---|---|---|---|
| A | Bể ngầm BTCT riêng cho chữa cháy | Bền, không chiếm mặt bằng, dự trữ chắc chắn | Chi phí đào, chống thấm; phải bơm toàn bộ |
| B | Bể chung sinh hoạt + chữa cháy (ống hút sinh hoạt đặt cao) | Nước luân chuyển, đỡ một bể | Rủi ro dùng lẹm dự trữ; phải kiểm soát mực nước |
| C | Bể thép lắp ghép trên mặt đất | Nhanh, tháo lắp được | Chiếm mặt bằng, ăn mòn, thẩm mỹ |
| D | Bể mái tự chảy cấp cho các tầng trên + bơm | Có áp lực ban đầu cho tầng trên | Tải trọng kết cấu mái; thường không đủ áp cho tầng sát mái |
| E | Lấy nước mạng đô thị (có xác nhận) + giảm dung tích bể | Giảm dung tích bể (`be-nuoc` có tham số bổ sung) | Phụ thuộc xác nhận của đơn vị cấp nước |

### 6.2 Cấu hình hệ thống
A: hệ riêng (họng nước & sprinkler riêng bơm, riêng trục) — độc lập, dễ thẩm định · B: hệ kết hợp chung bơm/trục — giảm ống & bơm, phải tính lưu lượng cộng dồn và được phép [DC] · C: mạng vòng thay nhánh cụt — giảm cỡ ống, tăng độ tin cậy.

### 6.3 Nhà cao tầng — phân vùng áp lực
| PA | Giải pháp | Khi nào hợp lý |
|---|---|---|
| A | 1 vùng + van giảm áp/màng tiết lưu tầng dưới | Nhà vừa (áp bơm ≲ 10–12 bar), rẻ nhất |
| B | 2+ vùng, bơm riêng từng vùng từ bể chung | Nhà rất cao; tránh áp lực vượt định mức thiết bị (PN16) |
| C | Bơm trung chuyển + bể trung chuyển ở tầng kỹ thuật | Nhà siêu cao; tăng độ tin cậy, tốn diện tích & tải trọng |

### 6.4 Cỡ ống ↔ bơm (tối ưu chi phí vòng đời)
Ống nhỏ → bơm cột áp lớn (vốn bơm & điện năng tăng); ống lớn → vốn ống tăng. So sánh bằng file cấu hình có `phuong_an` (xem `pccc/templates/vi-du/sprinkler-gara.json`, `hong-nuoc-chung-cu.json`): công cụ tính áp lực bơm, kW, chi phí ống + bơm + điện năng vòng đời và đề xuất PA rẻ nhất trong các PA đạt kỹ thuật.

### 6.5 Cấu hình bơm
B1: 1 điện + 1 diesel + bù áp · B2: 2 điện (2 nguồn) + bù áp · B3: 2 điện + 1 diesel + bù áp → `thuy_luc.py bom` lập bảng vốn/vòng đời, ưu nhược.
