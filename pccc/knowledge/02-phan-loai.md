# Phân loại kỹ thuật về cháy

Cập nhật: 2026-10-30 · Căn cứ chính: QCVN 06:2022/BXD + SĐ1:2023 (Chương 1–2, Phụ lục C, H), TCVN 7336:2021 Phụ lục A, QCVN 10:2025/BCA.

Phân loại là bước **quyết định mọi yêu cầu phía sau** (số lối ra, khoảng cách, khoang cháy, hệ thống phải trang bị). Sai phân loại = sai toàn bộ hồ sơ.

## 1. Chiều cao PCCC
- Định nghĩa (QCVN 06:2022, mục 1.4 — giải thích từ ngữ) [DC]: khoảng cách từ **mặt đường thấp nhất cho xe chữa cháy tiếp cận** tới **mép dưới lỗ mở (cửa sổ) trên tường ngoài của tầng trên cùng**, không kể tầng kỹ thuật trên cùng; khi không có lỗ mở thì lấy theo cao độ sàn/trần tầng trên cùng theo quy định tại định nghĩa.
- **Không** lấy chiều cao kiến trúc, cao độ đỉnh mái hay số tầng × chiều cao tầng.
- Cần có: mặt cắt + cao độ mặt đường xe chữa cháy (tổng mặt bằng). Thiếu → ghi giả định GĐ và hỏi lại.
- Các mốc thường gặp: 15 m · 21 m · 28 m · 50 m · 75 m · 150 m [DC] (F1.3 cao trên 75 m đến 150 m: theo Phụ lục A [TC]).

## 2. Bậc chịu lửa (I → V) và giới hạn chịu lửa cấu kiện
Bảng 4 QCVN 06:2022 “Sự phù hợp giữa bậc chịu lửa và giới hạn chịu lửa của cấu kiện” — giá trị tham khảo [DC]:

| Bậc | Bộ phận chịu lực (cột, tường, dầm) | Tường ngoài không chịu lực | Sàn giữa các tầng (kể cả hầm) | Mái: sàn mái / giàn, xà gồ | Tường trong buồng thang | Bản thang, chiếu nghỉ |
|---|---|---|---|---|---|---|
| I | R 150 | E 30 | REI 60 | RE 30 / R 30 | REI 150 | R 60 |
| II | R 120 | E 15 | REI 45 | RE 15 / R 15 | REI 120 | R 60 |
| III | R 90 | E 15 | REI 45 | RE 15 / R 15 | REI 90 | R 60 |
| IV | R 30 | E 15 | REI 15 | RE 15 / R 15 | REI 30 | R 15 |
| V | không quy định | | | | | |

Ký hiệu: **R** khả năng chịu lực, **E** tính toàn vẹn, **I** cách nhiệt (phút). Kiểm tra bằng Phụ lục F (giới hạn chịu lửa danh định theo chiều dày/lớp bảo vệ) [DC] hoặc kết quả thử nghiệm (TCVN 9311).
SĐ1:2023 có điều chỉnh liên quan nhà bậc I, S0 khi không đáp ứng chiều cao/diện tích khoang cháy (bản dự thảo nêu yêu cầu giới hạn chịu lửa kết cấu không thấp hơn Bảng 4) [TC — đối chiếu bản ban hành].

## 3. Cấp nguy hiểm cháy kết cấu (S0, S1, S2, S3)
Xác định theo tính nguy hiểm cháy của cấu kiện (K0–K3) [DC]. Nhà BTCT/thép bọc bảo vệ, vật liệu không cháy → thường S0. Mái/tường có vật liệu cháy (panel lõi xốp EPS/PU, gỗ) → S1–S3 → bất lợi cho khoang cháy & khoảng cách.

## 4. Nhóm nguy hiểm cháy theo công năng (F1 → F5) [DC]

| Nhóm | Phân nhóm (ví dụ) |
|---|---|
| F1 — nhà để ở | F1.1 nhà trẻ, mẫu giáo, bệnh viện nội trú, dưỡng lão · F1.2 khách sạn, nhà nghỉ, ký túc xá, nhà ở tập thể · F1.3 nhà chung cư · F1.4 nhà ở riêng lẻ |
| F2 — văn hóa, giải trí | F2.1 nhà hát, rạp chiếu phim, hội trường… có chỗ ngồi trong nhà · F2.2 bảo tàng, triển lãm, vũ trường… · F2.3/F2.4 như F2.1/F2.2 nhưng ngoài trời |
| F3 — dịch vụ công cộng | F3.1 thương mại · F3.2 ăn uống · F3.3 nhà ga · F3.4 phòng khám ngoại trú · F3.5 dịch vụ sinh hoạt · F3.6 thể thao trong nhà |
| F4 — giáo dục, khoa học, cơ quan | F4.1 trường phổ thông, đào tạo nghề · F4.2 đại học, cao đẳng · F4.3 cơ quan, văn phòng · F4.4 trạm chữa cháy |
| F5 — sản xuất, kho | F5.1 sản xuất, phòng thí nghiệm · F5.2 kho, gara không bảo dưỡng · F5.3 nhà nông nghiệp |

Nhà hỗn hợp: phân từng phần theo công năng + yêu cầu ngăn cách giữa các phần (xem `04-ngan-chay.md`). SĐ1:2023 mục 1.5.6: yêu cầu an toàn cháy theo **công năng thực tế** [TC].

## 5. Hạng nguy hiểm cháy nổ (nhà/gian phòng sản xuất & kho) — Phụ lục C QCVN 06
A, B (nguy hiểm cháy nổ: khí, hơi, bụi dễ cháy) · C1–C4 (nguy hiểm cháy, theo tải trọng cháy riêng) · D, E (nguy hiểm cháy vừa phải / thấp) [DC].
Tải trọng cháy riêng cho hạng C (tham khảo) [DC]: C1 > 2200 MJ/m² · C2 1401–2200 · C3 181–1400 · C4 1–180 (kèm điều kiện bố trí).
Không phân được hạng (thiếu danh mục hàng hóa/ quy trình) → hỏi chủ đầu tư; mặc định thiết kế bất lợi và ghi giả định.

## 6. Phân loại vật liệu xây dựng (Phụ lục B QCVN 06) [DC]
Tính cháy Ch1–Ch4 (và “không cháy”) · tính bắt cháy BC1–BC3 · tính lan truyền lửa trên bề mặt LT1–LT4 · khả năng sinh khói SK1–SK3 · độc tính ĐT1–ĐT4. Vật liệu hoàn thiện tường/trần/sàn trên đường thoát nạn bị giới hạn theo nhóm nhà & vị trí (sảnh, buồng thang, hành lang) — tra bảng tương ứng trong QCVN 06.

## 7. Nhóm nguy cơ cháy cho chữa cháy tự động (TCVN 7336:2021 Phụ lục A)
Tra theo công năng & tải trọng cháy: nhóm 1, 2, 3, 4.1, 4.2, 5, 6, 7 [TC — cấu trúc]. Ví dụ thường dùng [DC]: văn phòng, khách sạn, chung cư, bệnh viện → nhóm 1; gara ô tô, kho hàng không cháy trong bao bì cháy → nhóm 2. Thông số → `06-chua-chay-tu-dong.md`.

## 8. Hệ thống phải trang bị
- **QCVN 10:2025/BCA** (bắt buộc từ 30/12/2025): Phụ lục A — báo cháy tự động, chữa cháy tự động; các bảng khác cho họng nước, bình chữa cháy, loa thông báo… [TC].
- TCVN 3890:2023 Bảng A.1/A.2/A.3, B.1 — tham chiếu kỹ thuật [TC].
- Ghi rõ trong báo cáo: “Hệ thống X: BẮT BUỘC theo QCVN 10:2025/BCA, mục … [nhãn]” hoặc “KHÔNG bắt buộc — đề xuất tự nguyện vì …”.

## 9. Mẫu “Phiếu phân loại” (dán vào báo cáo)

| Tiêu chí | Giá trị | Căn cứ | Nhãn |
|---|---|---|---|
| Công năng chính / phụ | F… | QCVN 06:2022 Bảng … | |
| Chiều cao PCCC | … m (mặt đường xe CC +… → mép dưới cửa sổ tầng … +…) | QCVN 06:2022 mục 1.4 | |
| Số tầng nổi / hầm | … / … | | |
| Diện tích sàn lớn nhất 1 tầng / tổng | … / … m² | | |
| Khối tích | … m³ | | |
| Bậc chịu lửa (yêu cầu / thiết kế) | … / … | Bảng 4, Phụ lục H | |
| Cấp nguy hiểm cháy kết cấu | S… | | |
| Hạng nguy hiểm cháy nổ (nếu F5) | … | Phụ lục C | |
| Nhóm nguy cơ sprinkler | … | TCVN 7336:2021 Phụ lục A | |
| Hệ thống bắt buộc | báo cháy / sprinkler / họng nước / chống khói / … | QCVN 10:2025/BCA | |
| Thuộc diện thẩm định thiết kế về PCCC | có/không | NĐ 105/2025 | |
