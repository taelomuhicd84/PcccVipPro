# Kho tri thức PCCC — Mục lục & quy ước

Rà soát lần cuối: **2026-10-30** (tra cứu web; CHƯA mở được bản gốc các văn bản — xem nhãn từng số liệu).

## 1. Nhãn mức xác minh (bắt buộc gắn cho mọi số liệu quy định)

| Nhãn | Ý nghĩa | Được dùng thế nào |
|---|---|---|
| `[BG]` | Đã đối chiếu **bản gốc** (ghi rõ văn bản, mục, trang) | Dùng trực tiếp trong hồ sơ |
| `[TC]` | Xác nhận qua **nguồn thứ cấp** (trang luật, tài liệu hội thảo, bài kỹ thuật) | Dùng được để thiết kế sơ bộ; mở bản gốc trước khi ký hồ sơ |
| `[DC]` | Ghi nhớ chuyên môn, **chưa đối chiếu** | Chỉ để định hướng; BẮT BUỘC đối chiếu trước khi kết luận Đạt/Không đạt |
| `[QT]` | Tham khảo **quốc tế / thực hành / công thức kỹ thuật** (NFPA, EN, BS, SP, vật lý) | Dùng khi quy chuẩn VN không quy định hoặc cho phép (SĐ1:2023); phải nêu lập luận |

Khi trả lời, trích dẫn theo mẫu: `QCVN 06:2022/BXD, mục 3.2.6 [TC]` hoặc `TCVN 7336:2021, Bảng 2 [TC]`.
Nâng nhãn lên `[BG]` bằng skill `/pccc-cap-nhat-tri-thuc` khi người dùng cung cấp bản gốc (đặt vào `pccc/knowledge/nguon/`).

## 2. Danh mục

| File | Nội dung | Skill dùng nhiều nhất |
|---|---|---|
| `01-van-ban-phap-ly.md` | Luật, nghị định, thông tư, QCVN, TCVN còn hiệu lực + thứ tự tra cứu | mọi skill |
| `02-phan-loai.md` | Chiều cao PCCC, bậc chịu lửa, cấp S, nhóm F, hạng nguy hiểm cháy nổ, vật liệu | `pccc-phan-loai` |
| `03-thoat-nan.md` | Lối ra, khoảng cách, chiều rộng, buồng thang, lối ra khẩn cấp + thư viện phương án | `pccc-thoat-nan` |
| `04-ngan-chay.md` | Bộ phận ngăn cháy, khoang cháy, chống cháy lan, khoảng cách PCCC + phương án | `pccc-ngan-chay` |
| `05-cap-nuoc-chua-chay.md` | Họng nước trong/ngoài nhà, bể, trạm bơm, phương pháp thủy lực + phương án | `pccc-thuy-luc` |
| `06-chua-chay-tu-dong.md` | Sprinkler, drencher, khí, bọt, bếp, bình chữa cháy + phương án | `pccc-thuy-luc`, `pccc-chua-chay-dac-biet` |
| `07-chong-khoi.md` | Hút khói, tăng áp, cấp bù, công thức, bố trí quạt/ống/miệng + phương án | `pccc-hut-khoi` |
| `08-bao-chay.md` | Báo cháy tự động, loa thông báo, liên động + phương án | `pccc-bao-chay` |
| `09-chieu-sang-su-co-dien.md` | Chiếu sáng sự cố, chỉ dẫn thoát nạn, cấp điện & cáp cho PCCC | `pccc-bao-chay` |
| `10-tiep-can-chua-chay.md` | Đường & bãi xe chữa cháy, thang máy chữa cháy, cửa cứu nạn, họng tiếp nước | `pccc-tiep-can-chua-chay` |
| `11-cong-trinh-dac-thu.md` | Nhà > 50 m, gara (kể cả xe điện), chung cư, nhà xưởng/kho, BESS… | `pccc-phan-loai`, `pccc-thiet-ke` |
| `12-loi-thuong-gap.md` | Lỗi hay bị trả hồ sơ thẩm định + cách khắc phục | `pccc-tham-dinh` (agent) |
| `13-don-gia-tham-khao.md` | Cách dùng đơn giá để so sánh phương án (đơn giá GIẢ ĐỊNH) | `pccc-thuy-luc`, `pccc-hut-khoi` |
| `nguon/` | Nơi đặt bản gốc văn bản (PDF/DOCX) để đối chiếu | `pccc-cap-nhat-tri-thuc` |

Dữ liệu số dùng chung cho công cụ tính: `pccc/tools/du_lieu_tham_chieu.json` (cùng hệ nhãn `xm`).

## 3. Nguyên tắc dùng kho tri thức
1. Văn bản bắt buộc (Luật, NĐ, TT, QCVN) luôn ưu tiên hơn TCVN và tiêu chuẩn nước ngoài.
2. Không có trong kho ≠ không có quy định. Nếu không chắc → nói rõ, gắn `[DC]`, đề nghị người dùng cung cấp bản gốc.
3. Khi phát hiện văn bản mới/thay thế → cập nhật `01-van-ban-phap-ly.md`, ghi `pccc/memory/quyet-dinh.md`.
4. Mỗi file có dòng `Cập nhật:`; đổi nội dung thì đổi ngày.
