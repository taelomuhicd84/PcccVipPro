---
name: pccc-thiet-ke
description: Quy trình đầy đủ thiết kế / rà soát PCCC từ bản vẽ (ảnh, PDF) — đọc dữ liệu, phân loại công trình, kiểm tra thoát nạn, ngăn cháy, cấp nước & thủy lực, chữa cháy tự động, hút khói & tăng áp, báo cháy, tiếp cận chữa cháy; đưa nhiều phương án có so sánh kỹ thuật – chi phí và lập báo cáo. Dùng khi người dùng gửi bản vẽ hoặc yêu cầu thiết kế, thẩm tra, tư vấn phương án PCCC (phong chay chua chay) cho một công trình.
---

# /pccc-thiet-ke — Điều phối quy trình 8 bước

Đọc trước: `pccc/MODULE.md` (vai trò, nguyên tắc vàng, định dạng đầu ra).

## B0. Tiếp nhận (≤ 5 phút)
1. Liệt kê bản vẽ nhận được: loại (tổng mặt bằng, mặt bằng tầng, mặt cắt, mặt đứng, chi tiết thang, MEP), tỷ lệ, tầng.
2. Đặt mã dự án ngắn không dấu (VD `cc-hoang-mai-2026`) → tạo `pccc/du-an/<mã>/{input,output}` và `pccc/du-an/<mã>/README.md` (tên công trình, chủ đầu tư, giai đoạn thiết kế, ngày).
3. Nếu thiếu bản vẽ then chốt → vẫn làm tiếp phần có thể, đồng thời lập danh sách cần bổ sung:
   - thiếu mặt cắt → chưa chốt chiều cao PCCC;
   - thiếu tổng mặt bằng → chưa kiểm tra đường/bãi xe chữa cháy, khoảng cách PCCC;
   - thiếu bản vẽ MEP → hệ thống thiết kế mới theo phương án.

## B1. Đọc bản vẽ → dữ liệu công trình
Làm theo skill `pccc-doc-ban-ve`. Kết quả: `pccc/du-an/<mã>/du-lieu-cong-trinh.json` (mẫu `pccc/templates/du-lieu-cong-trinh.json`) + danh sách giả định GĐ-xx.

## B2. Phân loại
Skill `pccc-phan-loai` → Phiếu phân loại + danh mục hệ thống bắt buộc theo **QCVN 10:2025/BCA** (đối chiếu TCVN 3890:2023).

## B3. Kiến trúc an toàn cháy
- `pccc-thoat-nan` — số lối ra, phân tán, kích thước, khoảng cách (công cụ `thoat_nan.py`), buồng thang, lối ra khẩn cấp.
- `pccc-ngan-chay` — bậc chịu lửa, khoang cháy, bộ phận ngăn cháy, lỗ mở, trục kỹ thuật, mặt dựng, khoảng cách PCCC.
- `pccc-tiep-can-chua-chay` — đường & bãi xe, ô cửa tiếp cận, thang máy chữa cháy.

## B4. Hệ thống kỹ thuật
- `pccc-thuy-luc` — họng nước, sprinkler/drencher, bể, bơm (`thuy_luc.py`).
- `pccc-hut-khoi` — hút khói, cấp bù, tăng áp; tuyến ống, vị trí quạt & miệng gió (`hut_khoi.py`).
- `pccc-bao-chay` — báo cháy, loa, liên động, chiếu sáng sự cố, cấp điện & cáp.
- `pccc-chua-chay-dac-biet` — khí, bọt, bếp, bình chữa cháy.

## B5. Phương án
Mỗi ❌/🔶 hoặc hệ thống cần thiết kế → PA-A/B/C theo thư viện phương án trong các file chuyên đề `pccc/knowledge/` (mục “Thư viện phương án”); lượng hóa bằng `phuong_an` trong file cấu hình công cụ (công cụ tự lập bảng so sánh & đề xuất phương án rẻ nhất trong các PA đạt). Khuyến nghị cuối cùng cân nhắc thêm tiêu chí ngoài chi phí (`13-don-gia-tham-khao.md` §3).

## B6. Rà soát chéo
Tự rà theo `pccc/knowledge/12-loi-thuong-gap.md`. Công trình lớn/ quan trọng hoặc khi người dùng yêu cầu: giao subagent `pccc-tham-dinh` đọc báo cáo nháp và liệt kê điểm có thể bị trả hồ sơ.

## B7. Báo cáo
Skill `pccc-bao-cao` → `pccc/du-an/<mã>/output/bao-cao-pccc.md` (+ HTML nếu người dùng cần chia sẻ).

## B8. Ghi nhớ
Ghi nối vào `pccc/memory/du-an/<mã>.md` (quyết định, giả định đã được xác nhận) và `pccc/memory/bai-hoc.md` (bài học chung).

## Giao việc cho subagent (công trình lớn, nhiều chuyên môn)
Có thể chạy song song: `pccc-doc-ban-ve` (B1) → sau đó `pccc-kts-an-toan-chay`, `pccc-ks-cap-nuoc`, `pccc-ks-thong-gio-khoi`, `pccc-ks-dien-bao-chay` (B3–B5, mỗi agent nhận đường dẫn `du-lieu-cong-trinh.json` + phạm vi), cuối cùng `pccc-tham-dinh` (B6). Gộp kết quả theo định dạng `pccc/MODULE.md` §4; kiểm tra mâu thuẫn giữa các chuyên môn (VD vị trí trục khói vs thang thoát nạn, tải bể nước vs kết cấu).

## Trả lời cuối cho người dùng (trong chat)
1. Tóm tắt phân loại (3–5 dòng).
2. Bảng tổng hợp hạng mục: ✅/❌/🔶/⚠️ + số phương án đề xuất.
3. Khuyến nghị chính cho từng ❌ (1 dòng mỗi mục).
4. Giả định & câu hỏi cần trả lời.
5. Đường dẫn báo cáo chi tiết.
