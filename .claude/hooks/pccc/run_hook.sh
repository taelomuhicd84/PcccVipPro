#!/usr/bin/env bash
# Trình khởi chạy hook của module PCCC — FAIL-OPEN: thiếu Python / lỗi bất kỳ → KHÔNG chặn Claude.
# Dùng: bash run_hook.sh <ten_hook>   (session_start | prompt_context | guard_paths | lint_after_write)
# Tắt nhanh mọi hook PCCC: đặt biến môi trường PCCC_HOOKS_DISABLED=1
HOOK_NAME="${1:-}"
[ -z "$HOOK_NAME" ] && exit 0
[ "${PCCC_HOOKS_DISABLED:-0}" = "1" ] && exit 0
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || exit 0
SCRIPT="$DIR/$HOOK_NAME.py"
[ -f "$SCRIPT" ] || exit 0
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1 && \
     "$PY" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" </dev/null >/dev/null 2>&1; then
    exec "$PY" "$SCRIPT"
  fi
done
if command -v py >/dev/null 2>&1; then
  exec py -3 "$SCRIPT"
fi
exit 0
