#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$HERE/../.." && pwd -P)"
CP="$ROOT/checkpoints/2026-11-24-xbox-graphics"
WORK="$HOME/Documents/Codex/2026-11-24/leonida-3r1-gta-vi-macos-obiettivo/work"
SRC="$HOME/Developer/Leonida-NativePresent.pZEPof6d/source"
TOOL="$HOME/Developer/Leonida-3r1-Hybrid.vhvCuYrC/rustup/toolchains/1.98.1-aarch64-apple-darwin/bin"
export PATH="$TOOL:/opt/homebrew/opt/llvm/bin:/opt/homebrew/opt/lld/bin:$PATH"
export RUSTC="$TOOL/rustc"
export CARGO_HOME="$WORK/victory-cargo"
export XWIN_DIR="$HOME/.local/share/xwin-sdk"
export CX_BOTTLE_PATH="$WORK/bottles"
export CARGO_TARGET_X86_64_PC_WINDOWS_MSVC_LINKER=/opt/homebrew/opt/lld/bin/lld-link
export CC_x86_64_pc_windows_msvc=/opt/homebrew/opt/llvm/bin/clang-cl
export AR_x86_64_pc_windows_msvc=/opt/homebrew/opt/llvm/bin/llvm-lib
export CC_MASM_ASM_x86_64_pc_windows_msvc=/opt/homebrew/opt/llvm/bin/llvm-ml64
export CFLAGS_x86_64_pc_windows_msvc="/winsysroot \"$XWIN_DIR\""
export RUSTFLAGS="-C link-arg=/winsysroot:$XWIN_DIR"
unset CARGO_ENCODED_RUSTFLAGS VICTORY_WARP VICTORY_D3D12_WARP VICTORY_DUMP_TARGETS
export RUST_LOG=info
TARGET=x86_64-pc-windows-msvc
BOTTLE=Leonida-3r1
WINE=/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine
test -x "$TOOL/cargo"
test -x "$WINE"
test -d "$SRC"
python3 "$HERE/verify.py" --self-test
OUT="$(mktemp -d "$HOME/Developer/Leonida-Backbuffer.XXXXXXXX")"
echo "LOG: $OUT"
if [ -n "${LEONIDA_RESUME_DIR:-}" ]; then
    RESUME="$(cd "$LEONIDA_RESUME_DIR" && pwd -P)"
    test -f "$RESUME/build/$TARGET/release/victory.exe"
    grep -Fq 'Finished `release` profile' "$RESUME/build.log"
    grep -Fq 'Read the actual swap-chain buffer' "$RESUME/source/crates/victory-gpu/src/host.rs"
    grep -Fq 'VICTORY DXGI PRESENT:' "$RESUME/source/crates/victory-gpu/src/host.rs"
    export CARGO_TARGET_DIR="$RESUME/build"
    echo "REUSING EXISTING DIAGNOSTICS BUILD: $RESUME"
    shasum -a 256 "$CARGO_TARGET_DIR/$TARGET/release/victory.exe" | tee "$OUT/runtime-sha256.txt"
else
    mkdir "$OUT/source"
    rsync -a --exclude=.git --exclude=target "$SRC/" "$OUT/source/"
    cd "$OUT/source"
    git apply --check --unidiff-zero "$HERE/backbuffer.patch"
    git apply --unidiff-zero "$HERE/backbuffer.patch"
    grep -Fq 'VICTORY DXGI PRESENT:' crates/victory-gpu/src/host.rs
    export CARGO_TARGET_DIR="$OUT/build"
    cargo build --locked --offline --release --target "$TARGET" -p victory --features diagnostics 2>&1 | tee "$OUT/build.log"
fi
cd "$OUT"
llvm-dlltool -m i386:x86-64 -d "$CP/probes/d3d12_xs.def" -l d3d12_xs.lib
for mode in copy clear; do
    PROBE="$CP/probes/xbox_graphics.cpp"
    if [ "$mode" = clear ]; then PROBE="$HERE/xbox_clear.cpp"; fi
    # clang-cl treats absolute /Users paths as /U options.
    cp "$PROBE" "$mode.cpp"
    clang-cl --target=x86_64-pc-windows-msvc -fuse-ld=lld /winsysroot "$XWIN_DIR" \
        /std:c++17 /O2 /GS- /Zl "$mode.cpp" "/Fe$mode.exe" /link \
        /entry:probe_entry /subsystem:console /nodefaultlib kernel32.lib d3d12_xs.lib
    SCRATCH="$(mktemp -d "$CX_BOTTLE_PATH/$BOTTLE/drive_c/backbuffer.XXXXXXXX")"
    mkdir "$SCRATCH/capture"
    cp "$CARGO_TARGET_DIR/$TARGET/release/victory.exe" "$SCRATCH/"
    cp "$mode.exe" "$SCRATCH/"
    GUEST="C:\\$(basename "$SCRATCH")"
    export VICTORY_CAPTURE="$GUEST\\capture"
    export VICTORY_CAPTURE_FRAMES=1,2,3
    "$WINE" --bottle "$BOTTLE" --no-update --cx-app "$GUEST\\victory.exe" \
        run "$GUEST\\$mode.exe" --execute 2>&1 | tee "$OUT/$mode.log"
    grep -Fq 'title exited with 42' "$OUT/$mode.log"
    grep -Fq 'XBOX DEVICE11: PASS' "$OUT/$mode.log"
    test "$(grep -Fc 'VICTORY DXGI PRESENT: 0x00000000' "$OUT/$mode.log" || true)" -eq 3
    if [ "$mode" = clear ]; then grep -Fq 'XBOX GPU CLEAR: 3 FRAMES SUBMITTED' "$OUT/$mode.log"; fi
    mkdir "$OUT/$mode"
    cp "$SCRATCH/capture/"frame-*.png "$OUT/$mode/"
    python3 "$HERE/verify.py" "$mode" "$OUT/$mode" | tee "$OUT/$mode-validation.log"
done
echo "LEONIDA BACKBUFFER: PASS (92160 sampled RGB pixels)"
echo "LOG: $OUT"
