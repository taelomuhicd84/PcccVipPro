# STRUCTURE.md — Bản đồ repo PcccVipPro

## Nguyên tắc tổ chức (host)

```text
<repo>/
├── CLAUDE.md · STRUCTURE.md · MEMORY.md · README.md   ← DÙNG CHUNG: mỗi module 1 khối có đánh dấu
├── .gitignore · .gitattributes                        ← DÙNG CHUNG: khối "# <module>:begin/end"
├── .claude/
│   ├── settings.json                                  ← DÙNG CHUNG: gộp JSON (mỗi module thêm hook/quyền của mình)
│   ├── skills/<module>-*/SKILL.md                     ← tiền tố riêng từng module
│   ├── agents/<module>-*.md
│   └── hooks/<module>/
└── <module>/                                          ← toàn bộ phần riêng của module
```

| Loại tài nguyên | Chủ sở hữu | Cách hợp nhất |
|---|---|---|
| Thư mục module & tài sản Claude có tiền tố | module | sao chép nguyên khối — không thể va chạm |
| File văn bản dùng chung (`*.md`, `.git*`) | dự án chủ | mỗi module chèn/cập nhật **khối** của mình, không đụng phần còn lại |
| `.claude/settings.json` | dự án chủ | gộp JSON: hợp danh sách hook/quyền, không xóa của ai |

Chi tiết quy trình hợp nhất: `pccc/integration/HOP_NHAT.md`.

## Các module hiện có

<!-- pccc:begin · module pccc v1.0.0 · quản lý bởi pccc/integration/pccc_merge.py — sửa ở pccc/integration/blocks/, đừng sửa tay trong khối -->
## Module `pccc` — Trợ lý thiết kế PCCC

| Đường dẫn | Vai trò |
|---|---|
| `pccc/MODULE.md` | Bộ não module: vai trò, quy trình 8 bước, định dạng đầu ra, quy tắc |
| `pccc/STRUCTURE.md` | Bản đồ chi tiết của module (đọc file này khi cần biết file nào làm gì) |
| `pccc/knowledge/` | Kho tri thức quy chuẩn PCCC có nhãn xác minh `[BG]/[TC]/[DC]/[QT]` |
| `pccc/tools/` | Công cụ tính (Python thuần): `thuy_luc.py`, `hut_khoi.py`, `thoat_nan.py` |
| `pccc/templates/` | Phiếu dữ liệu công trình, mẫu báo cáo, ví dụ đầu vào công cụ |
| `pccc/memory/` | Bộ nhớ dài hạn của module (quyết định, bài học, theo dự án) |
| `pccc/du-an/` | Không gian làm việc từng dự án (`input/`, `output/`) |
| `pccc/integration/` | Hợp đồng & công cụ hợp nhất: `manifest.json`, `pccc_merge.py`, `pccc_doctor.py`, `HOP_NHAT.md` |
| `pccc/tests/` | Kiểm thử công cụ & tích hợp (`python3 -m unittest discover -s pccc/tests`) |
| `pccc/so_do_note.html` | Sơ đồ & ghi chú trực quan của module |
| `.claude/skills/pccc-*/` | Skill (gọi bằng `/pccc-...`) |
| `.claude/agents/pccc-*.md` | Subagent chuyên môn |
| `.claude/hooks/pccc/` | Hook của module (fail-open, chỉ tác động phần PCCC) |
<!-- pccc:end -->
