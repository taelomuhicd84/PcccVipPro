# Không gian làm việc theo dự án

Mỗi công trình một thư mục, tên ASCII không dấu, ngắn gọn: `pccc/du-an/<mã>/` (VD `cc-hoang-mai-2026`).

```text
pccc/du-an/<mã>/
├── README.md                    # tên công trình, chủ đầu tư, giai đoạn, trạng thái
├── du-lieu-cong-trinh.json      # phiếu dữ liệu (mẫu: pccc/templates/du-lieu-cong-trinh.json)
├── input/                       # bản vẽ gốc (PDF/PNG/DXF) — tên ASCII
├── tinh-toan/                   # file cấu hình công cụ (*.json) để chạy lại
├── output/                      # báo cáo, đầu ra công cụ, HTML chia sẻ
└── tmp/                         # file tạm (đã gitignore)
```

Mẫu khởi tạo nhanh: sao chép `pccc/du-an/_mau/`.
Bộ nhớ dự án: `pccc/memory/du-an/<mã>.md`.
Bản vẽ lớn: cân nhắc Git LFS; dữ liệu khách hàng nhạy cảm: chỉ dùng repo riêng tư.
