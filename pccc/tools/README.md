# Công cụ tính toán PCCC

Python ≥ 3.8, chỉ thư viện chuẩn. Chạy từ thư mục gốc repo. Mọi lệnh có `--help`, `--config <file.json>`, `--json`.
Mã thoát: `0` không có lỗi ❌ · `2` có hạng mục ❌ (tiện cho tự động hóa).

| Lệnh | Việc | Ví dụ đầu vào |
|---|---|---|
| `python3 pccc/tools/thuy_luc.py nhom` | Thông số nhóm nguy cơ sprinkler + nhãn | — |
| `python3 pccc/tools/thuy_luc.py ma-sat --q-l-s 30 --dn DN150` | Tổn thất 1 đoạn ống | — |
| `python3 pccc/tools/thuy_luc.py sprinkler --config …` | Mạng sprinkler dạng nhánh, áp lực bơm, so sánh PA | `templates/vi-du/sprinkler-gara.json` |
| `python3 pccc/tools/thuy_luc.py hong-nuoc --config …` | Họng nước trong nhà, tầng cần giảm áp | `templates/vi-du/hong-nuoc-chung-cu.json` |
| `python3 pccc/tools/thuy_luc.py be-nuoc --config …` | Dung tích & kích thước bể | `templates/vi-du/be-nuoc.json` |
| `python3 pccc/tools/thuy_luc.py bom --q-l-s 35 --h-m 70` | Công suất bơm, bơm bù áp, cấu hình B1/B2/B3 | — |
| `python3 pccc/tools/hut_khoi.py hanh-lang --config …` | Hút khói hành lang (TCVN 5687 PL L) | `templates/vi-du/hut-khoi-hanh-lang.json` |
| `python3 pccc/tools/hut_khoi.py phong --config …` | Hút khói gian phòng (PL L.2) | `templates/vi-du/hut-khoi-atrium.json` |
| `python3 pccc/tools/hut_khoi.py nfpa92 --config …` | Cột khói NFPA 92 (atrium) | `templates/vi-du/hut-khoi-atrium.json` |
| `python3 pccc/tools/hut_khoi.py tang-ap --config …` | Tăng áp buồng thang/khoang đệm | `templates/vi-du/tang-ap-buong-thang.json` |
| `python3 pccc/tools/hut_khoi.py ong-gio --q-m3-h 30000 --v-max 12 --t-c 300` | Kích thước ống gió | — |
| `python3 pccc/tools/thoat_nan.py duong-di --config …` | Khoảng cách thoát nạn từ đồ thị hành lang | `templates/vi-du/duong-di-tang-dien-hinh.json` |
| `python3 pccc/tools/thoat_nan.py so-nguoi --config …` | Số người tính toán | `templates/vi-du/so-nguoi.json` |
| `python3 pccc/tools/thoat_nan.py chieu-rong --config …` | Tổng chiều rộng lối ra | — |
| `python3 pccc/tools/thoat_nan.py phan-tan --config …` | Khoảng cách giữa các lối ra | — |

## So sánh phương án
Thêm vào file cấu hình:
```json
"phuong_an": [
  {"ma": "A", "ten": "…", "thay_doi": {}},
  {"ma": "B", "ten": "…", "thay_doi": {"ong_chinh_nhanh": "DN80", "khoi_luong_ong_m": {"DN80": 450}}}
]
```
`thay_doi` ghi đè đệ quy lên `thong_so`. Công cụ in bảng so sánh và đề xuất phương án có chi phí (đơn giá giả định hoặc `--don-gia <file>`) thấp nhất trong các phương án không có lỗi ❌.

## Dữ liệu
- `du_lieu_tham_chieu.json`: số liệu quy chuẩn/kỹ thuật dùng chung, mỗi giá trị có nhãn `xm` (BG/TC/DC/QT/VL). Công cụ in cảnh báo khi dùng giá trị [DC]/[QT].
- `don_gia_mac_dinh.json`: đơn giá GIẢ ĐỊNH (xem `pccc/knowledge/13-don-gia-tham-khao.md`).

Thêm công cụ mới: đặt trong thư mục này, import `pccc_common`, tên module mới có tiền tố `pccc_` nếu là thư viện dùng chung; thêm test vào `pccc/tests/`.
