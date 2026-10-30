# Thoát nạn — yêu cầu & thư viện phương án

Cập nhật: 2026-10-30 · Căn cứ chính: QCVN 06:2022/BXD + SĐ1:2023, Chương 3 (3.2 lối ra thoát nạn & lối ra khẩn cấp; 3.3 đường thoát nạn; 3.4 cầu thang & buồng thang), Phụ lục A (nhà cao), Phụ lục G (khoảng cách thoát nạn). Công cụ: `pccc/tools/thoat_nan.py`.

## 1. Khái niệm cần phân biệt
- **Lối ra thoát nạn**: dẫn ra ngoài trực tiếp, vào buồng thang bộ/thang bộ loại 3, vào hành lang/sảnh dẫn tới các lối đó, hoặc sang gian phòng/khoang cháy lân cận theo điều kiện quy chuẩn [DC].
- **Lối ra khẩn cấp**: không tính là lối ra thoát nạn (VD ban công/lô gia có điều kiện, cửa ra mái…) — dùng bổ sung, nhất là căn hộ ở cao [DC].
- **Hành lang cụt**: đoạn hành lang chỉ thoát được theo **một hướng**. Công cụ `thoat_nan.py duong-di` tự phân loại “giữa các lối ra” / “hành lang cụt”.
- **Buồng thang bộ**: L1 (có lỗ mở trên tường ngoài mỗi tầng), L2 (lấy sáng qua lỗ mở trên mái), N1 (vào buồng thang qua khoảng không ngoài nhà thông thoáng — ban công/lô gia hở), N2 (có áp suất dương khi cháy), N3 (vào qua khoang đệm có áp suất dương); **thang bộ** loại 1, 2 (bên trong để hở), loại 3 (ngoài nhà để hở) [DC].

## 2. Yêu cầu chính (kiểm tra từng mục, dẫn điều khoản khi kết luận)

### 2.1 Số lượng lối ra
- Tầng hầm, tầng nửa hầm: **≥ 2 lối ra thoát nạn** khi diện tích > 300 m² **hoặc** > 15 người (QCVN 06:2022 mục 3.2.6) [TC].
- SĐ1:2023: tại mỗi tầng hầm phải có **ít nhất 1 lối vào buồng thang bộ thoát nạn đi qua sảnh ngăn khói**, ngăn với không gian xung quanh bằng vách ngăn cháy loại 1 (hoặc giải pháp tương đương) [TC].
- Gian phòng / tầng của các nhóm F1.1, F1.2, F2, F3, F4 thường phải ≥ 2 lối ra khi vượt ngưỡng người (VD > 50 người) [DC].
- F1.3 (chung cư): cho phép 1 lối ra từ tầng khi tổng diện tích căn hộ trên tầng ≤ 500 m² và chiều cao PCCC ≤ 28 m (kèm loại buồng thang yêu cầu); cao hơn → buồng thang không nhiễm khói N1 và căn hộ ở độ cao > 15 m có lối ra khẩn cấp [DC].
- Nhà F1.3 thuộc Phụ lục A (cao): diện tích 1 tầng ≤ 2 000 m² (A.2.3) [TC].

### 2.2 Bố trí phân tán
- ≥ 2 lối ra phải phân tán: khoảng cách giữa các lối ra xa nhất **L ≥ 1,5·√P** (P: chu vi gian phòng/tầng) [DC]. Kiểm tra chéo: ≥ 1/2 đường chéo lớn nhất (≥ 1/3 nếu có sprinkler) theo IBC/NFPA [QT]. → `thoat_nan.py phan-tan`.

### 2.3 Kích thước
| Bộ phận | Yêu cầu tham khảo | Nhãn |
|---|---|---|
| Cửa lối ra thoát nạn | cao thông thủy ≥ 1,9 m; rộng ≥ 0,8 m (lớn hơn với gian phòng F1.1 đông người, cửa ra từ buồng thang ≥ bề rộng bản thang) | [DC] |
| Hành lang (phần nằm ngang) | rộng ≥ 1,2 m khi dùng cho > 15 người từ gian phòng F1 hoặc > 50 người từ nhóm khác; ≥ 0,7 m lối đi tới chỗ làm việc đơn lẻ; ≥ 1,0 m các trường hợp khác; cao thông thủy ≥ 2 m | [DC] |
| Bản thang | ≥ 1,35 m (nhà F1.1); ≥ 1,2 m (nhà có > 200 người trên tầng bất kỳ trừ tầng 1); ≥ 0,7 m (tới chỗ làm việc đơn lẻ); ≥ 0,9 m (còn lại); không nhỏ hơn bề rộng cửa trên đường thoát | [DC] |
| Bậc thang / độ dốc | mặt bậc ≥ 25 cm, chiều cao bậc ≤ 22 cm, độ dốc ≤ 1:1 (thang trong nhà) | [DC] |
| Khe hở giữa các vế thang | ≥ 75 mm (phục vụ kéo vòi chữa cháy) | [DC] |
| Tổng bề rộng theo số người | theo bảng/khả năng thông qua của QCVN 06 (theo nhóm, bậc chịu lửa, khối tích); kiểm tra chéo NFPA 101: 7,6 mm/người (thang), 5,1 mm/người (mặt bằng) | [DC] / [QT] |

### 2.4 Khoảng cách thoát nạn
- **F1.3 / F1.2** — Bảng G.1 QCVN 06:2022: từ cửa căn hộ/phòng ở tới lối ra gần nhất. Giá trị tham khảo (bậc I–II, S0): **40 m** khi cửa nằm giữa các buồng thang/lối ra; **25 m** khi cửa nằm trên hành lang cụt [DC]. Các bậc/cấp S thấp hơn có giới hạn nhỏ hơn [DC].
- Nhà thuộc Phụ lục A (cao): cửa căn hộ trên hành lang cụt → ≤ **15 m** tới lối ra gần nhất (A.2.19) [TC].
- Nhóm khác: các bảng G.2… theo nhóm, bậc chịu lửa, khối tích gian phòng, mật độ dòng người (một số bảng phân biệt “đi vào hành lang cụt”) [DC].
- Có/không tăng khoảng cách khi có chữa cháy tự động: chỉ áp dụng nếu chú thích bảng cho phép [DC].
- Cách đo: theo đường đi thực tế (tim lối đi, vòng qua đồ đạc cố định), không đo chim bay. → `thoat_nan.py duong-di`.

### 2.5 Cửa trên đường thoát nạn [DC]
- Mở theo hướng thoát nạn (trừ trường hợp quy chuẩn miễn, VD gian phòng ít người).
- Không dùng cửa cuốn, cửa trượt, cửa xoay, cửa nâng làm lối ra thoát nạn.
- Mở được từ bên trong không cần chìa; cửa buồng thang có cơ cấu tự đóng & chèn khe; giới hạn chịu lửa theo vị trí (VD cửa buồng thang EI 30 / cửa vào khoang đệm…).

### 2.6 Buồng thang & lối ra ngoài [DC trừ khi ghi khác]
- Nhà có chiều cao PCCC > 28 m: buồng thang **không nhiễm khói** (N1/N2/N3 theo điều kiện).
- Thang từ tầng hầm: tách khỏi thang tầng nổi (ngăn bằng tường/vách ngăn cháy tại tầng 1, lối ra ngoài riêng) hoặc giải pháp cho phép.
- Buồng thang phải có lối ra trực tiếp ra ngoài; ra qua sảnh tầng 1 chỉ khi đáp ứng điều kiện (SĐ1:2023 có quy định cho F1.2, F1.3, F2–F4 cao < 28 m khi không bố trí được lối ra riêng) [TC — đọc điều kiện chi tiết].
- Không bố trí phòng kỹ thuật, kho, ống dẫn khí cháy… trong buồng thang; vật liệu hoàn thiện không cháy.

### 2.7 Lối ra khẩn cấp [DC]
Ban công/lô gia có khoảng tường đặc theo quy định giữa các ô cửa, hoặc lối ra lên mái/ban công có thang… — dùng cho căn hộ F1.3 ở cao khi tầng chỉ có 1 lối ra thoát nạn.

### 2.8 Vật liệu hoàn thiện, chiếu sáng, chỉ dẫn
- Vật liệu hoàn thiện đường thoát nạn theo Phụ lục B/bảng vật liệu [DC].
- Chiếu sáng sự cố & biển chỉ dẫn → `09-chieu-sang-su-co-dien.md`.

## 3. Checklist đọc bản vẽ (thoát nạn)
1. Đánh dấu mọi lối ra thoát nạn trên từng mặt bằng (cửa ra ngoài, cửa buồng thang, thang loại 3).
2. Xác định loại buồng thang (L1/L2/N1/N2/N3) — có cửa sổ mỗi tầng? có khoang đệm? có quạt tăng áp?
3. Đếm số người mỗi gian/tầng (`thoat_nan.py so-nguoi`).
4. Đo khoảng cách theo tim hành lang → lập đồ thị nút/cạnh → `thoat_nan.py duong-di`.
5. Đo bề rộng cửa, hành lang, bản thang; chiều cao thông thủy (dầm, ống gió hạ trần!).
6. Kiểm tra chiều mở cửa, loại cửa, khóa.
7. Kiểm tra thang hầm tách thang nổi; sảnh ngăn khói tầng hầm (SĐ1:2023).
8. Kiểm tra lối ra từ buồng thang ra ngoài ở tầng 1.

## 4. Thư viện phương án khi không đạt

### 4.1 Khoảng cách thoát nạn vượt giới hạn
| PA | Giải pháp | Ưu | Nhược | Chi phí |
|---|---|---|---|---|
| A | Bổ sung buồng thang bộ mới (thường ở đầu hồi/cuối hành lang cụt) | Triệt để, tăng số lối ra | Mất diện tích sàn mỗi tầng (~20–30 m²/tầng), ảnh hưởng mặt bằng căn hộ | Cao |
| B | Thang bộ ngoài nhà loại 3 tại đầu hồi | Ít mất diện tích trong nhà, thi công nhanh | Ảnh hưởng mặt đứng; giới hạn áp dụng theo chiều cao/nhóm nhà [DC] | Trung bình |
| C | Tổ chức lại mặt bằng: dời vị trí buồng thang/cửa căn hộ, nối thông hành lang cụt thành hành lang giữa 2 lối ra | Không tăng thang | Phải sửa kiến trúc; hợp lý ở giai đoạn thiết kế cơ sở | Thấp–TB |
| D | Lối ra thoát nạn sang khoang cháy liền kề cùng tầng qua cửa ngăn cháy trong tường ngăn cháy | Tận dụng thang của khoang bên cạnh | Chỉ khi quy chuẩn cho phép tính là lối ra thoát nạn [DC]; phải đủ khả năng thông qua | Thấp |
| E | Giải pháp bù (VD tăng khoảng cách nhờ chữa cháy tự động) | Ít sửa kiến trúc | CHỈ khi chú thích bảng cho phép; nếu không → không dùng | Thấp |

### 4.2 Thiếu lối ra thứ hai
A: thêm buồng thang/cửa ra ngoài trực tiếp · B: thang ngoài nhà loại 3 · C: giảm diện tích/số người để thuộc trường hợp cho phép 1 lối ra (cam kết công năng, ghi vào hồ sơ) · D: lối ra sang khoang cháy lân cận (nếu được phép).

### 4.3 Lối ra không phân tán
A: dời một buồng thang/cửa · B: thêm lối ra ở vị trí xa · C: chia gian phòng lớn thành các gian có lối ra riêng.

### 4.4 Chiều rộng không đủ
A: mở rộng cửa/hành lang/bản thang · B: thêm lối ra để chia dòng người · C: giới hạn số người tính toán (biển báo sức chứa, cam kết vận hành).

### 4.5 Buồng thang sai loại (nhà > 28 m)
| PA | Giải pháp | Điều kiện / lưu ý |
|---|---|---|
| A | **N2** — tăng áp buồng thang (quạt + trục + xả áp/biến tần) | Phổ biến, ít ảnh hưởng mặt bằng; cần nguồn điện ưu tiên, kiểm soát lực mở cửa → `hut_khoi.py tang-ap` |
| B | **N3** — khoang đệm tăng áp mỗi tầng | Tốn diện tích khoang đệm; thường đi kèm thang máy chữa cháy |
| C | **N1** — vào buồng thang qua ban công/lô gia hở | Không cần quạt; cần mặt tiếp giáp ngoài trời, ảnh hưởng kiến trúc |

### 4.6 Thang hầm thông với thang nổi
A: tách thang hầm, lối ra ngoài riêng ở tầng 1 · B: ngăn tại tầng 1 bằng tường/vách ngăn cháy + cửa ngăn cháy, lối ra trực tiếp · C: sảnh ngăn khói tăng áp tại các tầng hầm (đồng thời đáp ứng SĐ1:2023).

Mỗi phương án trong báo cáo phải có: mô tả, điều khoản cho phép, ảnh hưởng kiến trúc/kết cấu/MEP, chi phí tương đối, rủi ro thẩm định, khuyến nghị.
