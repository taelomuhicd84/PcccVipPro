---
name: pccc-hop-nhat
description: Hợp nhất (merge) module PCCC với một dự án/repo khác của người dùng, hoặc nâng cấp module đã cài — phân tích va chạm trước (plan), cài/nâng cấp idempotent (install), đồng bộ sau git merge (sync), giải quyết xung đột (resolve), gỡ bỏ (uninstall), kiểm tra sau hợp nhất (doctor + test). Dùng khi người dùng nói hợp nhất, gộp, merge, tích hợp dự án/repo, nâng cấp module PCCC (hop nhat, gop du an).
---

# /pccc-hop-nhat — Hợp nhất với dự án khác mà không lỗi

Hướng dẫn đầy đủ: `pccc/integration/HOP_NHAT.md`. Hợp đồng: `pccc/integration/manifest.json`. Công cụ: `pccc/integration/pccc_merge.py`, `pccc_doctor.py`.

## Quy trình chuẩn
1. **Xác định hướng hợp nhất** (hỏi người dùng nếu chưa rõ):
   - **H1 (khuyến nghị)**: cài module PCCC VÀO dự án kia (dự án kia là repo chính).
   - **H2**: đưa dự án kia VÀO repo này (giữ lịch sử git cả hai bằng `git merge --allow-unrelated-histories`).
   - **H3**: tạo repo mới chứa cả hai.
2. **Chuẩn bị**: đích là git repo sạch (commit/stash trước); tạo nhánh mới, VD `git checkout -b hop-nhat-pccc`.
3. **Phân tích (không ghi gì)**: `python3 pccc/integration/pccc_merge.py plan --target <đích>` → đọc: file sẽ copy/cập nhật/xung đột, file dùng chung sẽ chèn khối/gộp, hook của dự án kia có thể tác động, quyền deny có thể chặn công cụ, va chạm tên skill/agent, khối của module khác. Báo tóm tắt cho người dùng trước khi làm tiếp.
4. **Thực hiện**:
   - H1/H3: `python3 pccc/integration/pccc_merge.py install --target <đích> --dry-run` rồi bỏ `--dry-run`.
   - H2: `git remote add khac <url|đường dẫn>` → `git fetch khac` → `git merge --allow-unrelated-histories khac/<nhánh>` → với **mỗi file dùng chung bị xung đột** (CLAUDE.md, STRUCTURE.md, MEMORY.md, README.md, .gitignore, .gitattributes, .claude/settings.json): giữ **phiên bản của dự án kia** (`git checkout --theirs <file>` khi đang ở repo này), rồi chạy `python3 pccc/integration/pccc_merge.py sync` để chèn lại khối PCCC và gộp hook/quyền → `git add` → commit.
5. **Kiểm tra**: `python3 pccc/integration/pccc_doctor.py --tests` (trong thư mục đích); `python3 pccc/integration/pccc_merge.py check`; mở phiên Claude Code mới trong đích để hook SessionStart chạy.
6. **Xung đột nâng cấp** (`*.pccc-new`): gộp tay nội dung vào file gốc (giữ sửa đổi cục bộ + thay đổi mới), rồi `python3 pccc/integration/pccc_merge.py resolve --target . <file>`.
7. **Ghi nhớ**: thêm mục vào `pccc/memory/quyet-dinh.md` (ngày, dự án đích, hướng hợp nhất, xung đột & cách xử lý).

## Quy tắc không được vi phạm
- Không sửa tay trong khối `pccc:begin … pccc:end`; không xóa hook/quyền của dự án kia; không đổi tên file/ thư mục của dự án kia.
- Không dùng `--force` khi chưa xem danh sách xung đột với người dùng.
- Nếu dự án kia cũng là “module” theo cùng chuẩn (có khối `<!-- <tên>:begin -->` riêng) → hai bộ khối cùng tồn tại; chỉ cần kiểm tra trùng tiền tố/ tên skill.
- Mọi bước phải hoàn tác được: làm trên nhánh riêng, commit theo từng bước.
