# HỢP NHẤT module PCCC với dự án khác — hướng dẫn đầy đủ

Công cụ: `pccc/integration/pccc_merge.py` · Kiểm tra: `pccc/integration/pccc_doctor.py` · Hợp đồng: `pccc/integration/manifest.json` · Skill: `/pccc-hop-nhat`

## 1. Vì sao hợp nhất không bị lỗi (6 cơ chế)
1. **Vùng sở hữu tách biệt (owned)** — mọi file của module nằm trong `pccc/`, `.claude/skills/pccc-*/`, `.claude/agents/pccc-*.md`, `.claude/hooks/pccc/`. Dự án khác không thể có file trùng tên ở đây (tiền tố riêng; hook `guard_paths` chặn tạo tài sản PCCC thiếu tiền tố).
2. **File dùng chung chỉ chứa “khối” của module** — `CLAUDE.md`, `STRUCTURE.md`, `MEMORY.md`, `README.md` có khối HTML-comment `pccc:begin` … `pccc:end`; `.gitignore`, `.gitattributes` có khối `# pccc:begin` … `# pccc:end`; `.claude/settings.json` được **gộp JSON** (chỉ thêm hook/quyền của module, không xóa của ai). Nguồn sự thật của mọi khối nằm trong `pccc/integration/` → luôn tái tạo được bằng `sync` (chạy bao nhiêu lần cũng cho cùng kết quả).
3. **Nâng cấp 3 chiều** — `pccc/integration/install-lock.json` lưu mã băm bản đã cài: file chỉ đổi ở nguồn → cập nhật; chỉ đổi ở đích → giữ nguyên; đổi cả hai → tạo `*.pccc-new` để gộp tay, không ghi đè; file nhật ký bộ nhớ → gộp hợp (union).
4. **Hook an toàn** — fail-open (thiếu Python/ lỗi → không chặn), chỉ tác động phần PCCC, tắt nhanh bằng `PCCC_HOOKS_DISABLED=1` hoặc `pccc/config.json`.
5. **Không phụ thuộc ngoài** — Python ≥ 3.8 thư viện chuẩn; tên file ASCII (tránh lỗi NFC/NFD giữa macOS/Windows/Linux); `.gitattributes` ép LF cho file của module (script `.sh` không hỏng trên Windows); giữ nguyên BOM/CRLF/thụt lề của file dự án kia.
6. **Kiểm tra tự động** — `plan` (trước), `check`/`doctor`/unittest (sau); SessionStart cảnh báo nếu tích hợp lệch sau `git merge`.

## 2. Bảng sở hữu
| Đường dẫn | Loại | Hành vi khi hợp nhất |
|---|---|---|
| `pccc/**` | owned | sao chép/ nâng cấp 3 chiều |
| `.claude/skills/pccc-*/**`, `.claude/agents/pccc-*.md`, `.claude/hooks/pccc/**` | owned | như trên |
| `CLAUDE.md`, `STRUCTURE.md`, `MEMORY.md`, `README.md` | shared (md-block) | chèn/cập nhật khối cuối file; tạo file nếu chưa có |
| `.gitignore`, `.gitattributes` | shared (hash-block) | như trên |
| `.claude/settings.json` | shared (json-merge) | gộp: thêm hook (nhận diện bằng `/.claude/hooks/pccc/`), hợp quyền, thêm `$schema` nếu thiếu |
| `pccc/integration/install-lock.json` | sinh ra ở đích | không sao chép từ nguồn |

Yêu cầu vị trí: `pccc/` phải nằm ở **gốc repo** cạnh `.claude/` (Claude Code đọc `.claude/` và `CLAUDE.md` ở gốc dự án).

## 3. Chọn hướng hợp nhất
| Hướng | Khi nào | Giữ lịch sử git của PCCC |
|---|---|---|
| **H1 — cài PCCC vào dự án kia** (khuyến nghị) | Dự án kia là repo chính | Không (có thể ghi commit nguồn trong message) |
| **H2 — đưa dự án kia vào repo này** | Muốn repo này là repo chính | Có (cả hai) |
| **H3 — repo mới chứa cả hai** | Bắt đầu sạch | Tùy cách làm |

### H1 — cài vào dự án kia
```bash
cd /duong-dan/du-an-kia && git status            # phải sạch; tạo nhánh mới
git checkout -b hop-nhat-pccc
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py plan    --target .
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py install --target . --dry-run
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py install --target .
python3 pccc/integration/pccc_doctor.py --tests
git add -A && git commit -m "Hợp nhất module PCCC v$(cat pccc/VERSION)"
```

### H2 — đưa dự án kia vào repo này (giữ lịch sử)
```bash
cd /duong-dan/PcccVipPro && git checkout -b hop-nhat-<ten-du-an>
git remote add khac /duong-dan/du-an-kia      # hoặc URL GitHub
git fetch khac
git merge --allow-unrelated-histories khac/main
# Xung đột chỉ có thể ở file DÙNG CHUNG. Với mỗi file bị xung đột:
git checkout --theirs CLAUDE.md README.md .gitignore .claude/settings.json   # giữ bản của dự án kia (chỉ các file đang xung đột)
python3 pccc/integration/pccc_merge.py sync   # chèn lại khối PCCC + gộp lại hook/quyền
git add -A && git commit
python3 pccc/integration/pccc_doctor.py --tests
```
Ghi chú: `--theirs` = phiên bản của nhánh đang được merge vào (dự án kia). File chỉ một bên có thì không xung đột.

### H3 — repo mới
Tạo repo mới → đưa dự án kia vào (copy hoặc `git merge`) → làm như H1 với `--target` là repo mới.

## 4. Sau mỗi `git pull` / `git merge` có đụng file dùng chung
```bash
python3 pccc/integration/pccc_merge.py check || python3 pccc/integration/pccc_merge.py sync
```
(Hook SessionStart cũng tự nhắc khi phát hiện lệch.)

## 5. Nâng cấp module đã cài (khi PcccVipPro có phiên bản mới)
```bash
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py install --target /duong-dan/du-an-da-cai --dry-run
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py install --target /duong-dan/du-an-da-cai
```
Kết quả: `update` (đã nâng cấp), `keep-local` (giữ sửa đổi của bạn), `union` (gộp nhật ký), `conflict` → mở `<file>.pccc-new`, gộp tay vào `<file>`, rồi:
```bash
python3 pccc/integration/pccc_merge.py resolve --target . <file>
```
`delete`: file đã bị bỏ ở phiên bản mới và bạn chưa sửa → xóa; `orphan`: đã bị bỏ nhưng bạn có sửa → giữ, tự quyết định.

## 6. Gỡ module
```bash
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py uninstall --target /duong-dan/du-an --dry-run
python3 /duong-dan/PcccVipPro/pccc/integration/pccc_merge.py uninstall --target /duong-dan/du-an
```
Gỡ khối khỏi file dùng chung (xóa file nếu do module tạo và nay rỗng), gỡ hook/quyền đã thêm, xóa file module chưa bị sửa; file đã sửa/ dữ liệu dự án được giữ lại và liệt kê (`--force` để xóa cả file đã sửa). Nội dung `.claude/settings.json` được khôi phục về ngữ nghĩa ban đầu (định dạng thụt lề có thể được chuẩn hóa).

## 7. Sự cố & cách xử lý
| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| `khối 'pccc' hỏng: 2 dòng begin…` | sửa tay/ merge làm nhân đôi khối | xóa bớt để còn đúng 1 cặp begin/end → `sync` |
| `JSON không hợp lệ` ở settings | conflict marker `<<<<<<<` còn trong file | sửa JSON (giữ bản dự án kia) → `sync` |
| Hook không chạy | chưa mở phiên mới; thiếu Python; `PCCC_HOOKS_DISABLED=1` | mở phiên Claude Code mới; cài Python 3.8+; trên Windows dùng Git Bash |
| Hook của dự án kia chặn ghi file PCCC | hook PreToolUse của họ | `plan` liệt kê sẵn; thống nhất ngoại lệ cho `pccc/**` |
| Quyền deny chặn `python3` | `permissions.deny` của dự án kia | `plan` cảnh báo; bổ sung ngoại lệ hoặc chạy công cụ thủ công |
| Còn `*.pccc-new` | xung đột nâng cấp chưa gộp | gộp tay → `resolve` |
| Skill/agent trùng tên | dự án kia dùng tiền tố `pccc-` | đổi tên bên dự án kia (module PCCC giữ tiền tố) |

## 8. Nếu dự án kia cũng làm theo chuẩn module này
Hai (hay nhiều) module cùng tồn tại tự nhiên: mỗi module có thư mục riêng, tiền tố riêng, marker riêng (`<!-- <tên>:begin -->`), fragment settings riêng. Khi tạo module mới cho dự án kia, sao chép mẫu `pccc/integration/` và đổi `module`, `owned`, `namespace`, `hook_command_marker` trong manifest — không dùng lại marker/tiền tố `pccc`.

## 9. Checklist sau hợp nhất
- [ ] `python3 pccc/integration/pccc_merge.py check` → 0
- [ ] `python3 pccc/integration/pccc_doctor.py --tests` → 0 lỗi
- [ ] `CLAUDE.md` của dự án chủ còn nguyên nội dung cũ + 1 khối PCCC ở cuối
- [ ] `.claude/settings.json`: hook & quyền của dự án chủ còn nguyên
- [ ] Mở phiên Claude Code mới: thấy dòng `[PCCC v…]` khi khởi động; gõ `/pccc-thiet-ke` có trong danh sách
- [ ] Ghi `pccc/memory/quyet-dinh.md`: ngày, dự án, hướng hợp nhất, xung đột đã xử lý
