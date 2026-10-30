# Chữa cháy tự động & phương tiện chữa cháy

Cập nhật: 2026-10-30 · Căn cứ: QCVN 10:2025/BCA (diện phải trang bị — bắt buộc) [TC], TCVN 3890:2023 [TC], TCVN 7336:2021 [TC], TCVN 7161/ISO 14520 [DC]. Công cụ: `thuy_luc.py sprinkler | nhom | be-nuoc | bom`.

## 1. Khi nào phải có chữa cháy tự động
- Tra **QCVN 10:2025/BCA Phụ lục A** (đã thu hẹp diện so với TCVN 3890:2023) [TC].
- TCVN 3890:2023: Bảng A.1 (toàn nhà), A.2 (hạng mục), A.3 (gian phòng); nhà **F1.3 cao ≤ 75 m chỉ bố trí đầu sprinkler tại cửa vào căn hộ** (không phủ trong căn hộ) [TC] — kiểm tra quy định tương ứng trong QCVN 10:2025.
- Không bắt buộc nhưng nên đề xuất (tự nguyện) khi giúp đạt yêu cầu khác (nếu chú thích quy chuẩn cho phép) hoặc giảm rủi ro tài sản/bảo hiểm.

## 2. Sprinkler nước — TCVN 7336:2021
### 2.1 Thông số theo nhóm nguy cơ (Bảng 2 — áp dụng chiều cao xếp hàng ≤ 5,5 m [TC])
| Nhóm | Cường độ phun l/(s·m²) | Lưu lượng tối thiểu l/s | Diện tích tính toán m² | Thời gian phút | Diện tích/đầu max m² | Khoảng cách max m |
|---|---|---|---|---|---|---|
| 1 | 0,08 [TC] | 10 [TC] | 60 [DC] | 30 [DC] | 12 [DC] | 4 [DC] |
| 2 | 0,12 [TC] | 30 [TC] | 120 [DC] | 60 [DC] | 12 [DC] | 4 [DC] |
| 3 | 0,24 [TC] | 60 [TC] | 240 [DC] | 60 [DC] | 12 [DC] | 4 [DC] |
| 4.1 | 0,30 [DC] | 110 [DC] | 360 [DC] | 60 [DC] | 9 [DC] | 3 [DC] |
| 4.2, 5, 6, 7 | theo bảng/tính riêng (bọt, kho cao…) [DC] | | | | | |

Nguồn số liệu dùng chung: `pccc/tools/du_lieu_tham_chieu.json` → `sprinkler_nhom`. Lưu lượng thiết kế cho bơm/bể = max(lưu lượng tính toán thủy lực, lưu lượng tối thiểu của nhóm) — thực hành phổ biến (VD gara nhóm 2 → 30 l/s × 60 phút = 108 m³) [TC/DC].

### 2.2 Bố trí (kiểm tra theo TCVN 7336:2021) [DC]
- Khoảng cách đầu phun ≤ giá trị bảng; đầu phun tới tường ≤ 1/2 khoảng cách; khoảng cách từ đầu phun tới trần/mái theo loại đầu phun.
- Vật cản (dầm sâu, ống gió, máng cáp rộng): bổ sung đầu phun bên dưới khi vật cản rộng vượt ngưỡng.
- Nhiệt độ tác động: thường 68 °C; khu nóng (bếp, mái tôn) chọn 79–93 °C hoặc cao hơn.
- Trạm van báo động: giới hạn số đầu phun mỗi trạm; công tắc dòng chảy + van chặn có giám sát cho từng tầng/khu; van xả & thử cuối tuyến.
- Hệ ướt (phổ biến); hệ khô/tiền kích hoạt (khu không được để nước trong ống: kho lạnh, phòng lưu trữ quan trọng).
- Kho xếp cao > 5,5 m: ngoài phạm vi Bảng 2 → tiêu chuẩn chuyên ngành (ESFR/in-rack theo NFPA 13 / FM DS 8-9) [QT].

### 2.3 Quy trình tính (công cụ `thuy_luc.py sprinkler`)
1. Xác định nhóm → cường độ, diện tích tính toán, lưu lượng min (preset kèm nhãn).
2. Đầu xa nhất: q = max(cường độ × diện tích/đầu, K·√p_min) → p = (q/K)².
3. Đi dọc ống nhánh: cộng tổn thất Hazen–Williams, tính q từng đầu = K·√p.
4. K tương đương nhánh → cân bằng các nhánh trên ống chính nhánh.
5. Ống cấp + cụm van + chênh cao → áp lực bơm; so lưu lượng min nhóm → Q bơm; thể tích nước.
6. So sánh phương án (cỡ ống, K-factor, khoảng cách đầu) bằng `phuong_an`.

## 3. Drencher (màn nước) [DC]
Dùng tạo màn ngăn cháy tại lỗ mở, bảo vệ kết cấu/kính, ngăn cháy lan; lưu lượng tính theo chiều dài màn (l/s trên mỗi mét) và thời gian theo TCVN 7336:2021 → cộng vào bể & bơm.

## 4. Chữa cháy bằng khí [DC / QT]
| Chất | Ưu | Nhược / lưu ý |
|---|---|---|
| HFC-227ea (FM-200) | Bình ít, xả nhanh (~10 s), an toàn ở nồng độ thiết kế | Khí nhà kính — lộ trình cắt giảm HFC (Kigali); giá tăng |
| FK-5-1-12 (Novec 1230 và tương đương) | GWP thấp, biên an toàn cao | 3M ngừng sản xuất PFAS từ cuối 2025 — chọn nhà cung cấp FK-5-1-12 khác, kiểm tra nguồn cung [QT] |
| IG-541 / IG-55 / IG-100 (khí trơ) | Thân thiện môi trường, không sản phẩm phân hủy | Nhiều bình, áp cao, cần xả áp phòng; thời gian xả ~60–120 s |
| CO₂ | Rẻ, hiệu quả | **Nguy hiểm chết người** ở nồng độ chữa cháy — chỉ phòng không người, cần khóa liên động & cảnh báo trễ |
Yêu cầu chung: phòng kín (thử quạt cửa), xả áp phòng, trễ xả + báo động, nút dừng khẩn, liên động ngắt điều hòa/đóng van gió → TCVN 7161 / ISO 14520 / NFPA 2001.

## 5. Chữa cháy bằng bọt [DC]
Kho xăng dầu, nhà chứa nhiên liệu, khu đỗ máy bay/ trực thăng… → TCVN 7336 (phần bọt) và tiêu chuẩn chuyên ngành.

## 6. Bếp ăn thương mại [QT]
Hệ thống chữa cháy chụp hút & ống thải bếp (hóa chất ướt, UL 300) + ngắt gas tự động; ống thải khói bếp bọc chịu lửa khi qua khoang cháy khác.

## 7. Bình chữa cháy & phương tiện ban đầu
- QCVN 10:2025/BCA: **bỏ yêu cầu dự trữ ≥ 10% số bình** [TC]; số lượng, loại, vị trí theo quy chuẩn [TC — vị trí].
- Nguyên tắc bố trí (tham khảo TCVN 3890:2023) [DC]: chọn bình theo loại đám cháy (A chất rắn, B chất lỏng, C khí, E/điện, F/dầu ăn); đặt ở nơi dễ thấy, dễ lấy, gần lối ra; khoảng cách di chuyển tới bình và số bình mỗi tầng theo bảng; phòng điện dùng CO₂/khí; bếp dùng bình loại F/bột phù hợp.
- Phương tiện cứu nạn, cứu hộ (mặt nạ lọc độc, đèn pin, búa…) theo QCVN 10:2025/BCA [TC — phạm vi].

## 8. Thư viện phương án
### 8.1 Sprinkler
| PA | Giải pháp | Khi nào |
|---|---|---|
| A | K80, lưới 3,4 × 3,4 m, ống nhỏ — bơm lớn | Vốn ống thấp |
| B | K80, ống chính nhánh/ống cấp tăng 1 cỡ — bơm nhỏ | Giảm cột áp, giảm kW, ít ồn |
| C | K115 (hoặc K-factor lớn hơn) — giảm áp đầu phun, có thể tăng khoảng cách trong giới hạn | Nhóm 2–3, trần cao |
| D | Mạng vòng/lưới thay nhánh cụt | Diện tích lớn, cân bằng áp tốt |
| E | Hệ khô/tiền kích hoạt | Khu cấm nước đọng/ nguy cơ rò rỉ |

### 8.2 Bảo vệ phòng điện/ máy chủ
A: khí FK-5-1-12/HFC-227ea · B: khí trơ IG-541 · C: sprinkler tiền kích hoạt + báo khói sớm (ASD) · D: chỉ báo cháy sớm + bình CO₂ (khi không bắt buộc chữa cháy tự động).
