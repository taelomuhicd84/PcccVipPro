# STRUCTURE — Bản đồ chi tiết module `pccc`

Phạm vi sở hữu (khai báo trong `pccc/integration/manifest.json`): `pccc/` · `.claude/skills/pccc-*/` · `.claude/agents/pccc-*.md` · `.claude/hooks/pccc/`.
Mọi thứ khác trong repo thuộc dự án chủ hoặc module khác.

```text
pccc/
├── MODULE.md                  Bộ não: vai trò, nguyên tắc vàng, quy trình 8 bước, định dạng đầu ra (import vào CLAUDE.md)
├── STRUCTURE.md               File này
├── VERSION                    Phiên bản module (khớp manifest.json)
├── CHANGELOG.md               Lịch sử thay đổi module
├── config.json                Bật/tắt hook, ngày rà soát tri thức, mặc định số phương án
├── so_do_note.html            Sơ đồ & ghi chú trực quan (mở bằng trình duyệt, chạy offline)
├── knowledge/                 Kho tri thức có nhãn [BG]/[TC]/[DC]/[QT]
│   ├── 00-muc-luc.md          Quy ước nhãn, danh mục
│   ├── 01-van-ban-phap-ly.md  Văn bản hiện hành, thứ tự tra cứu
│   ├── 02-phan-loai.md … 11-cong-trinh-dac-thu.md   Yêu cầu + thư viện phương án theo chuyên đề
│   ├── 12-loi-thuong-gap.md   Lỗi hay bị trả hồ sơ
│   ├── 13-don-gia-tham-khao.md
│   └── nguon/                 Bản gốc văn bản để đối chiếu (README hướng dẫn)
├── tools/                     Công cụ tính (Python thuần, CLI, --json)
│   ├── pccc_common.py         Tiện ích chung (Hazen–Williams, ống gió, phương án, bảng)
│   ├── thuy_luc.py            sprinkler | hong-nuoc | be-nuoc | bom | ma-sat | nhom
│   ├── hut_khoi.py            hanh-lang | phong | nfpa92 | tang-ap | ong-gio
│   ├── thoat_nan.py           duong-di | so-nguoi | chieu-rong | phan-tan
│   ├── du_lieu_tham_chieu.json  Số liệu dùng chung có nhãn xác minh
│   ├── don_gia_mac_dinh.json  Đơn giá GIẢ ĐỊNH để so sánh phương án
│   └── README.md
├── templates/
│   ├── du-lieu-cong-trinh.json  Phiếu dữ liệu công trình
│   ├── bao-cao-phuong-an.md     Mẫu báo cáo
│   └── vi-du/                   Ví dụ đầu vào công cụ (có 'phuong_an')
├── memory/                    Bộ nhớ dài hạn (INDEX.md nạp mỗi phiên; nhật ký merge=union)
│   ├── INDEX.md · quyet-dinh.md · bai-hoc.md
│   └── du-an/                 Bộ nhớ theo dự án
├── du-an/                     Không gian làm việc từng công trình (input/ tinh-toan/ output/)
│   └── _mau/                  Mẫu thư mục dự án
├── integration/               Hợp đồng & công cụ hợp nhất
│   ├── manifest.json          owned / shared / exclude / merge_union / namespace
│   ├── settings.fragment.json Hook + quyền của module (gộp vào .claude/settings.json)
│   ├── blocks/                Nguồn các khối chèn vào file dùng chung
│   ├── pccc_merge.py          status | check | plan | install | sync | resolve | uninstall
│   ├── pccc_doctor.py         Kiểm tra sức khỏe module (--tests)
│   └── HOP_NHAT.md            Hướng dẫn hợp nhất chi tiết
└── tests/                     unittest: công cụ, hợp nhất, hook

.claude/
├── skills/pccc-*/SKILL.md     13 skill: thiet-ke (điều phối), doc-ban-ve, phan-loai, thoat-nan, ngan-chay,
│                              thuy-luc, hut-khoi, bao-chay, tiep-can-chua-chay, chua-chay-dac-biet,
│                              bao-cao, cap-nhat-tri-thuc, hop-nhat
├── agents/pccc-*.md           6 subagent: doc-ban-ve, kts-an-toan-chay, ks-cap-nuoc, ks-thong-gio-khoi,
│                              ks-dien-bao-chay, tham-dinh
└── hooks/pccc/                run_hook.sh (fail-open) + session_start, prompt_context, guard_paths, lint_after_write
```

## Luồng dữ liệu
Bản vẽ (`du-an/<mã>/input/`) → `du-lieu-cong-trinh.json` → phân loại → kiểm tra theo `knowledge/` → file cấu hình `tinh-toan/*.json` → `tools/*.py` (bảng tính + so sánh phương án) → `output/bao-cao-pccc.md` → bài học vào `memory/`.

## Hook (đăng ký trong `.claude/settings.json`, nguồn `integration/settings.fragment.json`)
| Sự kiện | Script | Tác dụng | Khi lỗi |
|---|---|---|---|
| SessionStart | `session_start.py` | Tóm tắt ≤ 7 dòng: phiên bản, dự án gần đây, tri thức cũ, tích hợp lệch, xung đột chưa gộp | bỏ qua |
| UserPromptSubmit | `prompt_context.py` | Chỉ khi câu hỏi về PCCC/hợp nhất: 1 dòng nhắc quy trình | bỏ qua |
| PreToolUse (Write/Edit) | `guard_paths.py` | Chặn sửa tay khối quản lý; chặn tài sản PCCC thiếu tiền tố | bỏ qua |
| PostToolUse (Write/Edit) | `lint_after_write.py` | Kiểm tra frontmatter skill/agent, JSON, Python, CRLF, khối đánh dấu | bỏ qua |
Tắt tất cả: `PCCC_HOOKS_DISABLED=1`; tắt từng phần: `pccc/config.json`.
