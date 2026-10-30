---
name: pccc-ngan-chay
description: Kiểm tra ngăn cháy & chống cháy lan theo QCVN 06:2022/BXD (bậc chịu lửa và giới hạn chịu lửa cấu kiện, diện tích khoang cháy Phụ lục H, tường/vách/sàn/cửa ngăn cháy, khoang đệm, lỗ mở, trục kỹ thuật, ống xuyên khoang, atrium, mặt dựng, khoảng cách PCCC giữa các nhà) và đề xuất nhiều phương án. Dùng khi hỏi về ngăn cháy, khoang cháy, chịu lửa, cháy lan (ngan chay, khoang chay).
---

# /pccc-ngan-chay — Ngăn cháy, khoang cháy, chống cháy lan

Tri thức: `pccc/knowledge/04-ngan-chay.md` (yêu cầu + thư viện phương án §8), `02-phan-loai.md` (Bảng 4).

## Quy trình
1. **Bậc chịu lửa**: bảng cấu kiện chính (cột, dầm, sàn, tường chịu lực, tường buồng thang, bản thang, mái) — giới hạn chịu lửa yêu cầu vs giải pháp (chiều dày, lớp bảo vệ cốt thép, sơn/ốp chống cháy kết cấu thép, chứng nhận).
2. **Khoang cháy**: khoanh ranh giới trên mỗi tầng, cộng diện tích (kể cả thông tầng, thang cuốn) → so Phụ lục H (F, bậc, S, chiều cao PCCC).
3. **Ngăn cách công năng**: các phần F khác nhau, gara, phòng kỹ thuật nguy hiểm (trạm biến áp, máy phát, bồn dầu, kho, phòng bơm, phòng rác).
4. **Lỗ mở & xuyên qua**: cửa/ màn/ van ngăn cháy đúng loại; chèn bịt ống, cáp; van ngăn cháy trên ống gió; trục kỹ thuật & giếng thang.
5. **Mặt dựng**: băng tường đặc/ ô văng giữa các tầng, chèn ngăn cháy tại sàn của vách kính, vật liệu ốp.
6. **Khoảng cách PCCC** tới nhà lân cận (Phụ lục E) — cần tổng mặt bằng.
7. **Phương án**: mỗi ❌ → ≥ 2 phương án (§8); khi dùng drencher làm ranh giới khoang → chuyển lưu lượng sang `pccc-thuy-luc` để tính bể/bơm.

## Đầu ra
- Bảng giới hạn chịu lửa cấu kiện (yêu cầu / thiết kế / đánh giá / căn cứ).
- Sơ đồ khoang cháy dạng bảng: | Tầng | Khoang | Diện tích | Giới hạn | Đánh giá |.
- Danh sách lỗ mở/xuyên khoang và cách bảo vệ.
- Khối phương án & khuyến nghị (ghi rõ chi phí tương đối, ảnh hưởng kiến trúc).

## Lưu ý
- Vật liệu/cấu kiện ngăn cháy phải có chứng nhận & giấy phép lưu thông (TT 63/2025/TT-BXD, hiệu lực 16/02/2026) [TC].
- “Tăng diện tích khoang cháy nhờ sprinkler” chỉ dùng nếu chú thích Phụ lục H cho phép — hiện chưa xác nhận [DC].
