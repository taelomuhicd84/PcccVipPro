# Bảo vệ chống khói — hút khói, tăng áp, cấp bù

Cập nhật: 2026-10-30 · Căn cứ: QCVN 06:2022/BXD **Phụ lục D** + SĐ1:2023 (D.1.7) [TC], TCVN 5687:2010 Phụ lục L (công thức) [TC] — kiểm tra TCVN 5687:2024 [DC]; tham khảo NFPA 92, BS EN 12101-6 [QT]. Công cụ: `pccc/tools/hut_khoi.py`.

## 1. Khi nào phải có (Phụ lục D QCVN 06 — kiểm tra từng trường hợp) [DC]
**Hút xả khói** thường yêu cầu cho:
- Hành lang & sảnh chung của nhà có buồng thang không nhiễm khói; hành lang dài không có thông gió tự nhiên (cửa sổ mở được đủ diện tích) theo ngưỡng chiều dài/nhóm nhà.
- Gian phòng có người thường xuyên không có cửa sổ mở được, phòng lớn (hội trường, trung tâm thương mại, phòng trưng bày…), kho/sản xuất có hạng nguy hiểm cháy — theo ngưỡng diện tích.
- Tầng hầm, gara kín; không gian thông tầng (atrium).

**Cấp không khí (tăng áp)** thường yêu cầu cho:
- Buồng thang **N2**; khoang đệm của buồng thang **N3**; giếng thang máy (khi không có khoang đệm tăng áp) trong nhà có buồng thang không nhiễm khói; giếng & sảnh thang máy chữa cháy; khoang đệm/sảnh tầng hầm; cấp bù cho hệ hút khói.

## 2. Thông số chính
| Thông số | Giá trị | Nhãn |
|---|---|---|
| Áp suất dư khi cháy (buồng thang N2, khoang đệm N3, giếng thang máy…) | **20 Pa → 50 Pa** (D.11, D.12) | [TC] |
| Vận tốc gió qua cửa mở của khoang đệm | ≥ 1,3 m/s | [DC] |
| Thứ tự khởi động | hút khói khởi động **trước** cấp không khí 20–30 s | [DC] |
| Cấp bù | không thiếu quá 30% lưu lượng khối lượng hút (≥ 70%), cấp ở phần dưới gian phòng, vận tốc thấp | [DC] |
| Chiều dài hành lang phục vụ bởi 1 miệng hút | ≤ 45 m (thẳng), ≤ 30 m (có góc), ≤ 20 m (vòng) | [DC] |
| Vị trí miệng hút trong hành lang | dưới trần, không thấp hơn mép trên cửa đi | [DC] |
| Quạt hút khói | chịu nhiệt độ khói theo thời gian quy định (VD 400 °C – 2 h, hoặc theo tính toán) | [DC] |
| Ống gió & van hút khói | giới hạn chịu lửa EI theo vị trí (trong/ngoài khoang cháy phục vụ, trục đứng) | [DC] |
| Miệng xả khói ra ngoài | cao hơn mái/ cách xa miệng lấy gió tăng áp & cửa sổ theo quy định | [DC] |
| Lực mở cửa trên đường thoát nạn khi tăng áp | ≤ 100 N (EN 12101-6), ≤ 133 N (NFPA 101) | [QT] |
| SĐ1:2023 D.1.7 | cho phép thay đổi yêu cầu Phụ lục D khi thiết kế chống khói theo tiêu chuẩn được phép áp dụng | [TC] |

## 3. Công thức (đã cài trong `hut_khoi.py`)
### 3.1 Hút khói hành lang/sảnh — TCVN 5687:2010 Phụ lục L [TC]
- Nhà ở: **G = 3420 · B · H^1,5 · n** (kg/h)
- Nhà công cộng, hành chính, sản xuất: **G = 4300 · B · H^1,5 · n · Kd** (kg/h)
- B: chiều rộng cánh cửa lớn (từ hành lang vào buồng thang/ra ngoài), m; H: chiều cao cửa, m; n: hệ số theo tổng chiều rộng cánh cửa lớn (Bảng L1) [phải tra]; Kd: hệ số thời gian mở cửa [phải tra].
### 3.2 Hút khói gian phòng — TCVN 5687:2010 Phụ lục L.2 [TC]
- **G = 678,8 · Pf · y^1,5 · Ks** (kg/h); Pf: chu vi đám cháy, m; y: khoảng cách từ sàn tới mép dưới lớp khói, m; Ks: hệ số (thường 1,0).
- Phạm vi: Pf ≤ 12 m và y ≤ 4 m — ngoài phạm vi dùng L.3 hoặc mô hình cột khói [TC].
### 3.3 Đổi sang lưu lượng thể tích [VL]
- ρ_khói = 353 / (273 + t), t: nhiệt độ khói (°C); L (m³/h) = G / ρ. Cộng rò rỉ ống/van đóng các tầng không cháy (thực hành 10–20%, tính chi tiết với trục phục vụ nhiều tầng) [QT].
### 3.4 Không gian lớn/atrium — NFPA 92 (kiểm tra chéo) [QT]
- Cột khói đối xứng: Qc = 0,7·Q; z_l = 0,166·Qc^(2/5); m = 0,071·Qc^(1/3)·z^(5/3) + 0,0018·Qc (z > z_l).
- Chống thủng lớp khói: V_max/miệng = 4,16·γ·d^(5/2)·(ΔT/T₀)^(1/2) → số miệng tối thiểu.
### 3.5 Tăng áp — EN 12101-6 [QT] (giới hạn Δp theo QCVN 06 [TC])
- Cửa đóng: Q = 0,83 · ΣA_rò · Δp^0,5 (m³/s); diện tích khe cửa: cửa đơn mở vào 0,01 m², mở ra 0,02 m², cửa đôi 0,03 m², cửa tầng thang máy 0,06 m².
- Cửa mở: Q = v · A_cửa + rò rỉ các cửa đóng còn lại; chọn lưu lượng lớn hơn của 2 tiêu chí, cộng 15% rò rỉ ống.
- Kiểm soát quá áp khi mọi cửa đóng: van xả áp hoặc biến tần + cảm biến chênh áp; kiểm tra lực mở cửa F = F_đóng cửa + W·A·Δp / (2(W − d)).

## 4. Hướng dẫn bố trí (ống gió đi như nào, quạt & miệng gió đặt đâu)
### 4.1 Hút khói hành lang
- **Trục đứng** hút khói riêng (không dùng chung thông gió thường), đặt sát hành lang, ưu tiên gần **giữa** đoạn hành lang hoặc tại đầu hành lang cụt; mỗi tầng có **van hút khói thường đóng** (mở tầng cháy) đặt dưới trần, cao hơn mép trên cửa.
- Bố trí sao cho mọi điểm trên hành lang nằm trong bán kính phục vụ (≤ 45/30/20 m tùy cấu hình) [DC]; tránh đặt miệng hút ngay cạnh cửa buồng thang tăng áp (gió tăng áp bị hút tắt).
- **Quạt** hút khói đặt trên mái/tầng kỹ thuật trên cùng (khói tự nổi lên, đường ống ngắn) trong phòng quạt ngăn cháy hoặc ngoài trời có che chắn; có van một chiều/van gió tại cửa quạt.
- **Miệng xả** hướng lên/ngang, xa miệng lấy gió tăng áp, cửa sổ, cửa lấy gió AHU.
- **Cấp bù** cho hành lang: từ trục cấp riêng/ cửa mở tự động ở phần dưới hành lang, hoặc dùng gió tràn từ buồng thang tăng áp khi phương pháp thiết kế cho phép [DC].
### 4.2 Hút khói tầng hầm/gara
- Chia **khoang khói** (màn ngăn khói/dầm sâu), mỗi khoang có miệng hút phân bố đều ở phần trên; cấp bù ở phần dưới, xa miệng hút.
- Có thể kết hợp thông gió thường ngày (quạt 2 tốc độ chịu nhiệt), tự chuyển chế độ khi có tín hiệu báo cháy.
- Phương án **quạt phản lực (jet fan)**: giảm ống gió, tăng chiều cao thông thủy; cần mô phỏng/thiết kế theo tiêu chuẩn được phép (SĐ1:2023 D.1.7) [TC/QT].
### 4.3 Tăng áp buồng thang
- Quạt lấy gió tươi ở vị trí **không bị khói** (tầng thấp phía đón gió hoặc mái cách xa miệng xả khói).
- Nhà thấp/vừa: cấp 1 điểm; nhà cao: **cấp nhiều điểm** (trục cấp dọc buồng thang, miệng cấp cách 2–3 tầng) để áp suất đều [QT].
- Kiểm soát quá áp (van xả áp ra ngoài/ biến tần) để Δp ≤ 50 Pa và lực mở cửa đạt.
### 4.4 Ống gió & van
- Ống thép (mạ kẽm/đen) kín khít; đoạn đi ngoài trục kỹ thuật hoặc qua khoang cháy khác phải bọc/ đạt giới hạn chịu lửa EI theo quy định [DC].
- Van hút khói (NC) trên ống hút khói; van ngăn cháy (NO) trên ống thông gió thường khi xuyên bộ phận ngăn cháy.
- Vận tốc khuyến nghị: trục/ống thép ≤ 10–15 m/s; miệng hút 5–8 m/s; miệng cấp bù ≤ 1 m/s tại vùng người [QT] → `hut_khoi.py ong-gio`.
### 4.5 Liên động điều khiển (gắn với báo cháy)
Tín hiệu cháy (tầng/khoang) → mở van hút khói tầng cháy → chạy quạt hút khói → sau 20–30 s chạy quạt cấp bù & tăng áp [DC] → dừng AHU/quạt thông gió thường, đóng van ngăn cháy → thang máy về tầng 1 → điều khiển tay tại phòng trực & tại chỗ; giám sát trạng thái quạt/van.

## 5. Thư viện phương án
### 5.1 Hút khói hành lang
| PA | Giải pháp | Ưu | Nhược |
|---|---|---|---|
| A | 1 trục đứng tập trung + ống ngang hai phía | Ít quạt, ít trục | Ống ngang dài, tốn trần; rò rỉ nhiều |
| B | 2 trục đứng theo khoang khói (2 đầu hành lang) | Ống ngang ngắn, quạt nhỏ, dự phòng | Thêm trục & quạt |
| C | Thông gió tự nhiên (cửa sổ/ô thoáng mở tự động đủ diện tích) | Không quạt, rẻ vận hành | Chỉ khi quy chuẩn cho phép; phụ thuộc gió, mặt đứng |
| D | Quạt hút khói xả ngang từng tầng | Không cần trục | Nhiều quạt, khó bảo trì; ít dùng |

### 5.2 Gara/tầng hầm
A: ống gió hút khói + cấp bù (kết hợp thông gió thường, quạt 2 cấp) · B: quạt phản lực (jet fan) + trục hút tập trung · C: hệ riêng thông gió & hút khói (đắt, đơn giản điều khiển).

### 5.3 Atrium/sảnh lớn
A: hút cơ khí trên đỉnh + cấp bù tự nhiên dưới · B: thông gió tự nhiên qua cửa mái tự mở · C: kết hợp; tính đối chứng TCVN 5687 Phụ lục L.2 & NFPA 92 (ví dụ: `pccc/templates/vi-du/hut-khoi-atrium.json`).

### 5.4 Tăng áp buồng thang
A: quạt cố định + van xả áp trọng lực · B: biến tần + cảm biến chênh áp · C: phân đoạn buồng thang (nhà rất cao) → so sánh bằng `pccc/templates/vi-du/tang-ap-buong-thang.json`.
