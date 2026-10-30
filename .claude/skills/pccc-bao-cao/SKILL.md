---
name: pccc-bao-cao
description: Lập báo cáo/thuyết minh phương án PCCC theo mẫu chuẩn của module (phân loại, bảng kiểm tra từng hạng mục có căn cứ & nhãn xác minh, khối phương án và bảng so sánh, tính toán tái lập, giả định, câu hỏi, danh sách cần đối chiếu) — xuất Markdown và tùy chọn HTML để chia sẻ. Dùng khi cần viết báo cáo, thuyết minh, tổng hợp kết quả PCCC (bao cao, thuyet minh).
---

# /pccc-bao-cao — Báo cáo phương án PCCC

Mẫu: `pccc/templates/bao-cao-phuong-an.md`. Định dạng: `pccc/MODULE.md` §4.

## Quy trình
1. Sao chép mẫu → `pccc/du-an/<mã>/output/bao-cao-pccc.md`; điền theo thứ tự mục của mẫu.
2. Mỗi kết luận có căn cứ + nhãn; mỗi số liệu tính toán có lệnh công cụ và đường dẫn file cấu hình (`pccc/du-an/<mã>/tinh-toan/*.json`) để người khác chạy lại.
3. Mỗi hạng mục ❌/🔶/hệ thống thiết kế mới: khối phương án (≥ 2) + bảng so sánh + khuyến nghị.
4. Tổng hợp đầu báo cáo: bảng hạng mục | trạng thái | phương án khuyến nghị | chi phí tương đối | rủi ro thẩm định.
5. Cuối báo cáo: giả định GĐ-xx, câu hỏi, danh sách số liệu `[DC]` cần đối chiếu bản gốc, bước tiếp theo, tuyên bố trách nhiệm (1 đoạn).
6. Kiểm tra nhất quán: số liệu trong bảng = đầu ra công cụ = phiếu dữ liệu công trình; tên tầng/trục thống nhất với bản vẽ.
7. Nếu người dùng cần chia sẻ: xuất HTML tự chứa (không tài nguyên ngoài) cùng thư mục `output/`.

## Văn phong
Tiếng Việt kỹ thuật, câu ngắn, bảng nhiều hơn đoạn văn; đơn vị SI (m, m², l/s, Pa, bar, kW); số thập phân dùng dấu phẩy trong văn bản báo cáo (bảng xuất từ công cụ dùng dấu chấm — giữ nguyên, ghi chú một lần).
