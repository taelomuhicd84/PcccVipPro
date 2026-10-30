## PCCC — Trợ lý thiết kế Phòng cháy chữa cháy (module `pccc`)

Biến Claude Code thành kỹ sư thiết kế PCCC: nhận bản vẽ → đọc dữ liệu → phân loại công trình → kiểm tra thoát nạn, ngăn cháy, cấp nước chữa cháy, chống khói, báo cháy, tiếp cận chữa cháy… → đưa **nhiều phương án** có so sánh kỹ thuật & chi phí → lập báo cáo.

**Bắt đầu nhanh**
1. Mở repo bằng Claude Code, gửi bản vẽ (ảnh/PDF) rồi gõ `/pccc-thiet-ke`.
2. Công cụ tính: `python3 pccc/tools/thuy_luc.py --help` · `python3 pccc/tools/hut_khoi.py --help` · `python3 pccc/tools/thoat_nan.py --help`.
3. Kiểm tra sức khỏe module: `python3 pccc/integration/pccc_doctor.py`.
4. Hợp nhất với dự án khác: đọc `pccc/integration/HOP_NHAT.md` hoặc gõ `/pccc-hop-nhat`.

Sơ đồ trực quan: `pccc/so_do_note.html`. ⚠️ Kết quả là công cụ hỗ trợ kỹ thuật; hồ sơ phải do người có chứng chỉ hành nghề kiểm tra, ký và cơ quan có thẩm quyền thẩm định.
