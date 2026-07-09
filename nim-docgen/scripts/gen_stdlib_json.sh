#!/usr/bin/env bash
set -uo pipefail
ROOT="/Users/kalaverin/src/lang/nim"
OUT="$ROOT/.kimi/skills/nim-docgen/references/json"
LIST="/tmp/stdlib_modules.txt"
LOG="$OUT/.gen.log"
STDOUT_LOG="$OUT/.stdout.log"
NIM="$ROOT/bin/nim"
rm -rf "$OUT"
mkdir -p "$OUT"
: > "$LOG"
: > "$STDOUT_LOG"

gen_one() {
  local src="$1"
  local rel="${src%.nim}.json"
  local dst="$OUT/$rel"
  mkdir -p "$(dirname "$dst")"
  local extra=""
  local base
  base=$(basename "$src")
  if [[ "$src" == lib/js/* ]] || [[ "$base" =~ ^(jsbigints|jsfetch|jsformdata|jsheaders|jsutils)\.nim$ ]]; then
    extra="--backend:js"
  fi
  if "$NIM" jsondoc \
      --noImportdoc \
      --errormax:3 \
      --hint:Conf:off \
      --hint:Path:off \
      --hint:Processing:off \
      --hint:XDeclaredButNotUsed:off \
      --warning:UnusedImport:off \
      $extra \
      -o:"$dst" "$src" >> "$LOG" 2>&1; then
    echo "OK $src"
  else
    echo "FAIL $src" >&2
    rm -f "$dst"
  fi
}
export -f gen_one
export OUT NIM LOG

xargs -P 4 -I {} bash -c 'gen_one "$@"' _ {} < "$LIST" | tee -a "$STDOUT_LOG"
