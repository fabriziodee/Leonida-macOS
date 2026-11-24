#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$HERE/../.." && pwd -P)"
WORK="$HOME/Documents/Codex/2026-11-24/leonida-3r1-gta-vi-macos-obiettivo/work"
RESUME="$HOME/Developer/Leonida-Backbuffer.nTnBgpYt"
export PATH="/opt/homebrew/opt/llvm/bin:/opt/homebrew/opt/lld/bin:$PATH"
export CX_BOTTLE_PATH="$WORK/bottles"
export RUST_LOG=info
unset VICTORY_WARP VICTORY_D3D12_WARP VICTORY_DUMP_TARGETS VICTORY_SKIP_PIPELINES
WINE=/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine
BOTTLE=Leonida-3r1
BIN="$RESUME/build/x86_64-pc-windows-msvc/release/victory.exe"
test "$(shasum -a 256 "$BIN" | awk '{print $1}')" = bbccb2cf79bbbbcc41845c88f44564adf1266c10527a2138401601f4e2291639
OUT="$(mktemp -d "$HOME/Developer/Leonida-Depth.XXXXXXXX")"
echo "LOG: $OUT"
cd "$OUT"
python3 "$HERE/generate.py" shaders.h
cp "$HERE/xbox_depth.cpp" draw.cpp
llvm-dlltool -m i386:x86-64 -d "$ROOT/checkpoints/2026-11-24-xbox-graphics/probes/d3d12_xs.def" -l d3d12_xs.lib
clang-cl --target=x86_64-pc-windows-msvc -fuse-ld=lld /winsysroot "$HOME/.local/share/xwin-sdk" /std:c++17 /O2 /GS- /Zl draw.cpp /Fedraw.exe /link /entry:probe_entry /subsystem:console /nodefaultlib kernel32.lib d3d12_xs.lib 2>&1 | tee build.log
SCRATCH="$(mktemp -d "$CX_BOTTLE_PATH/$BOTTLE/drive_c/depth.XXXXXXXX")"
mkdir "$SCRATCH/capture"
cp "$BIN" draw.exe "$SCRATCH/"
GUEST="C:\\$(basename "$SCRATCH")"
export VICTORY_CAPTURE="$GUEST\\capture"
export VICTORY_CAPTURE_FRAMES=5,6,7,8
"$WINE" --bottle "$BOTTLE" --no-update --cx-app "$GUEST\\victory.exe" run "$GUEST\\draw.exe" --execute 2>&1 | tee execution.log
grep -Fq 'title exited with 42' execution.log
grep -Fq 'XBOX DEPTH: 8 FRAMES SUBMITTED' execution.log
test "$(grep -Fc 'VICTORY DXGI PRESENT: 0x00000000' execution.log)" -eq 8
cp -R "$SCRATCH/capture" "$OUT/capture"
python3 "$HERE/verify_depth.py" "$ROOT/experiments/xbox-backbuffer/verify.py" "$OUT"
echo "LOG: $OUT"
