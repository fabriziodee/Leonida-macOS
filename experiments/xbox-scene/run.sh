#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$HERE/../.." && pwd -P)"
# Explicit local paths are supported for independent synthetic reproduction.
WORK="${LEONIDA_WORK_DIR:-$HOME/Documents/Codex/2026-11-24/leonida-3r1-gta-vi-macos-obiettivo/work}"
RESUME="${LEONIDA_RESUME_DIR:-$HOME/Developer/Leonida-Backbuffer.nTnBgpYt}"
export PATH="/opt/homebrew/opt/llvm/bin:/opt/homebrew/opt/lld/bin:$PATH"
export CX_BOTTLE_PATH="${CX_BOTTLE_PATH:-$WORK/bottles}"
export RUST_LOG=info
unset VICTORY_WARP VICTORY_D3D12_WARP VICTORY_DUMP_TARGETS VICTORY_SKIP_PIPELINES
WINE="${CROSSOVER_WINE:-/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine}"
BOTTLE="${LEONIDA_BOTTLE:-Leonida-3r1}"
BIN="${LEONIDA_VICTORY_EXE:-$RESUME/build/x86_64-pc-windows-msvc/release/victory.exe}"
SDK="${XWIN_DIR:-$HOME/.local/share/xwin-sdk}"
OUT_PARENT="${LEONIDA_OUTPUT_DIR:-$HOME/Developer}"
EXPECTED="${LEONIDA_RUNTIME_SHA256:-bbccb2cf79bbbbcc41845c88f44564adf1266c10527a2138401601f4e2291639}"
fail() { printf '%s\n' "$*" >&2; exit 2; }
[[ -f "$BIN" ]] || fail "Missing diagnostics runtime: $BIN"
[[ -x "$WINE" ]] || fail "Missing CrossOver executable: $WINE"
[[ -d "$SDK" ]] || fail "Missing xwin SDK: $SDK"
[[ -d "$CX_BOTTLE_PATH/$BOTTLE/drive_c" ]] || fail "Missing bottle drive_c: $CX_BOTTLE_PATH/$BOTTLE"
[[ -d "$OUT_PARENT" ]] || fail "Missing output directory: $OUT_PARENT"
for tool in python3 clang-cl llvm-dlltool shasum; do
    command -v "$tool" >/dev/null || fail "Missing tool: $tool"
done
ACTUAL="$(shasum -a 256 "$BIN" | awk '{print $1}')"
[[ "$ACTUAL" == "$EXPECTED" ]] || fail "Runtime hash mismatch: expected $EXPECTED, got $ACTUAL"
OUT="$(mktemp -d "$OUT_PARENT/Leonida-Scene.XXXXXXXX")"
printf '%s\n' "$ACTUAL" > "$OUT/runtime-sha256.txt"
git -C "$ROOT" rev-parse HEAD > "$OUT/leonida-commit.txt"
echo "LOG: $OUT"
cd "$OUT"
python3 "$ROOT/experiments/xbox-uv/generate.py" shaders.h
python3 "$HERE/scene.py" scene_vertices.h
cp "$HERE/xbox_scene.cpp" draw.cpp
llvm-dlltool -m i386:x86-64 -d "$ROOT/checkpoints/2026-11-24-xbox-graphics/probes/d3d12_xs.def" -l d3d12_xs.lib
clang-cl --target=x86_64-pc-windows-msvc -fuse-ld=lld /winsysroot "$SDK" /std:c++17 /O2 /GS- /Zl draw.cpp /Fedraw.exe /link /entry:probe_entry /subsystem:console /nodefaultlib kernel32.lib d3d12_xs.lib 2>&1 | tee build.log
SCRATCH="$(mktemp -d "$CX_BOTTLE_PATH/$BOTTLE/drive_c/scene.XXXXXXXX")"
mkdir "$SCRATCH/capture"
cp "$BIN" draw.exe "$SCRATCH/"
GUEST="C:\\$(basename "$SCRATCH")"
export VICTORY_CAPTURE="$GUEST\\capture"
export VICTORY_CAPTURE_FRAMES=5,6,7,8
"$WINE" --bottle "$BOTTLE" --no-update --cx-app "$GUEST\\victory.exe" run "$GUEST\\draw.exe" --execute 2>&1 | tee execution.log
grep -Fq 'title exited with 42' execution.log
grep -Fq 'XBOX SCENE: 8 FRAMES SUBMITTED' execution.log
test "$(grep -Fc 'VICTORY DXGI PRESENT: 0x00000000' execution.log)" -eq 8
cp -R "$SCRATCH/capture" "$OUT/capture"
python3 "$HERE/verify_scene.py" "$ROOT/experiments/xbox-backbuffer/verify.py" "$OUT" | tee "$OUT/validation.log"
echo "LOG: $OUT"
