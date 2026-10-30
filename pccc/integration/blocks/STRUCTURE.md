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
