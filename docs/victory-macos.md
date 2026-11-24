# VIctory smoke test on Apple Silicon

Use a dedicated 64-bit CrossOver bottle with D3DMetal selected. The smoke
test checks the x64 host capabilities and the VIctory executable entry path
using two synthetic programs. The host probe also clears a 4x4
RGBA8 render target, copies it to a CPU-readable buffer, waits for a fence
(up to ten seconds), and checks every pixel. The optional GPU binaries below
also exercise VIctory's texture upload and translated compute shaders.

Build [VIctory](https://github.com/Marvisak/VIctory) for
`x86_64-pc-windows-msvc`. The verified upstream revision was
`d2a4bae1f49533ef5cb512fd1b1ba1513f2e1989`. On macOS, use the pinned Rust
toolchain, LLVM's `lld-link`, `clang-cl`, `llvm-lib` and `llvm-ml64`, and
an xwin SDK prepared with `--use-winsysroot-style`.

Run the smoke test with a local VIctory executable and the directory that
contains your dedicated bottle.

```sh
XWIN_DIR="$HOME/.local/share/xwin-sdk" \
  scripts/run_victory_macos_smoke.sh /path/to/bottles TestBottle /path/to/victory.exe
```

The probes report AVX2, D3D12 initialization, shader model and mesh
shader support. A successful launch prints
`VIctory synthetic title entry reached` and `title exited with 42`.
On an M1 Max, macOS 27.3 and CrossOver 26.3, the probes detected AVX2,
Shader Model 6.6 and Mesh Shader Tier 1, and the synthetic program
returned 42. On 24 November 2026, the extended probe at `33829eca0`
compiled with clang-cl and the xwin SDK, then ran in a copy of the
D3DMetal-configured bottle. The smoke script exited successfully and printed:

```text
GPU clear/readback: PASS (16 RGBA pixels)
VIctory synthetic title entry reached
title exited with 42
```

The last line is the synthetic title's exit status as reported by VIctory.
The runtime binary was the release build from the revision above. This
validation was AI-assisted. See the [backend evaluation](macos-backends.md)
for the evidence behind the current first-boot path.

Boot and visual verification of GTA VI require an authorized Xbox Series
game directory whose executable, companion DLLs and assets are already
readable. GTA VI boot and menus remain unverified on this setup.

## Texture uploads and compute shaders on the M1 Max

The [VIctory macOS fork](https://github.com/pragyaangaur/VIctory-macOS/tree/f5660fdcfdd6eb5cb6495be47a23af9aa30f5617)
includes the [staging upload fix](https://github.com/pragyaangaur/VIctory-macOS/commit/af22e5d3a12c49a3fccc6812b06260715edcab70).
On our M1 Max, the unpatched fork returned positive zero for `v_sin_f32(-0)`.
The [local patch](../patches/victory-macos-m1.patch) preserves the input's exact
negative-zero bits after the host sine, adds a half-precision assertion and
prints a marker after the texture fixture has compared all four rows.
VIctory's code is GPL-3.0-or-later.

From the Leonida-macOS root, set `VICTORY_SRC` to a separate checkout at the
pinned revision and export `XWIN_DIR` for the prepared Windows SDK. These commands
use Rust 1.98.1 with the Windows MSVC target and Homebrew LLVM and LLD.
Export `VICTORY_SRC`, `XWIN_DIR`, `BOTTLES_DIR` and `BOTTLE_NAME` before running.
The explicit Bash subprocess below also works when pasted into macOS's default Zsh.

```bash
bash <<'BASH'
set -euo pipefail
: "${VICTORY_SRC:?}" "${XWIN_DIR:?}" "${BOTTLES_DIR:?}" "${BOTTLE_NAME:?}"
leonida_root="$(pwd -P)"
git -C "$VICTORY_SRC" apply --check "$leonida_root/patches/victory-macos-m1.patch"
git -C "$VICTORY_SRC" apply "$leonida_root/patches/victory-macos-m1.patch"
cd "$VICTORY_SRC"
export CARGO_TARGET_X86_64_PC_WINDOWS_MSVC_LINKER="$(brew --prefix lld)/bin/lld-link"
export CC_x86_64_pc_windows_msvc="$(brew --prefix llvm)/bin/clang-cl"
export AR_x86_64_pc_windows_msvc="$(brew --prefix llvm)/bin/llvm-lib"
export CC_MASM_ASM_x86_64_pc_windows_msvc="$(brew --prefix llvm)/bin/llvm-ml64"
export CFLAGS_x86_64_pc_windows_msvc="/winsysroot \"$XWIN_DIR\""
export CARGO_ENCODED_RUSTFLAGS="-Clink-arg=/winsysroot:$XWIN_DIR"
target=x86_64-pc-windows-msvc
export CARGO_TARGET_DIR="$(mktemp -d)"
cargo build --release --locked --target "$target" -p victory
cargo build --release --locked --target "$target" -p victory-shader -p victory-gpu --tests
release="$CARGO_TARGET_DIR/$target/release"
gpu_tests=("$release"/deps/victory_gpu-*.exe)
shader_tests=("$release"/deps/victory_shader-*.exe)
[[ ${#gpu_tests[@]} -eq 1 && -f "${gpu_tests[0]}" ]]
[[ ${#shader_tests[@]} -eq 1 && -f "${shader_tests[0]}" ]]
VICTORY_REQUIRE_EXTENDED=1 VICTORY_GPU_TEST_EXE="${gpu_tests[0]}" VICTORY_SHADER_TEST_EXE="${shader_tests[0]}" \
  "$leonida_root/scripts/run_victory_macos_smoke.sh" "$BOTTLES_DIR" "$BOTTLE_NAME" "$release/victory.exe"
BASH
```

Use an existing D3DMetal bottle for `BOTTLES_DIR` and `BOTTLE_NAME`.
The texture fixture sends four distinct rows through VIctory's command list
and checks 64 returned bytes. The two shader fixtures dispatch DXIL on the
hardware adapter, including NaN, infinity, large turns and signed zero.

## Independent M4 Max reproduction · 24 November 2026

The [independent M4 Max report in issue #1](https://github.com/fabriziodee/Leonida-macOS/issues/1#issuecomment-7142660029) by `edmondja` covers Mac Studio M4 Max (40 GPU cores, 128 GB RAM), macOS 27.2.1, CrossOver 26.3 / D3DMetal 3.0, at Leonida-macOS `912df590`. Both the upstream VIctory build `d2a4bae1` and patched macOS fork `f5660fd` reported AVX2, D3D12 creation, SM 6.6, 16 matching RGBA pixels and synthetic exit 42. The patched fork also reported the 64-byte texture comparison. The initial report did not distinguish WARP from hardware execution. The [follow-up instrumented run](https://github.com/fabriziodee/Leonida-macOS/issues/1#issuecomment-7144872577) identified the same hardware adapter by LUID in each call (DXGI name AMD Compatibility Mode, a D3DMetal compatibility identifier, not a physical AMD GPU). All 25 f32 cases in four calls and 16 f16 cases in three calls passed on hardware. Only WARP was unavailable (EnumWarpAdapter returned 0x887a0004). The previous smoke filter was too strict: it rejected optional WARP skips. The revised patch incorporates the contributor's test-only adapter diagnostic; the script requires positive hardware markers for all expected calls and case counts and rejects hardware skips. A rerun of the combined revised script is still pending. The Bash/Zsh example remains corrected. No game files were used, and real game boot remains unverified.
