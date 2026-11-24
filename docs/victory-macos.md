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

```bash
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
VICTORY_GPU_TEST_EXE="${gpu_tests[0]}" VICTORY_SHADER_TEST_EXE="${shader_tests[0]}" \
  "$leonida_root/scripts/run_victory_macos_smoke.sh" "$BOTTLES_DIR" "$BOTTLE_NAME" "$release/victory.exe"
```

Use an existing D3DMetal bottle for `BOTTLES_DIR` and `BOTTLE_NAME`.
The texture fixture sends four distinct rows through VIctory's command list
and checks 64 returned bytes. The two shader fixtures dispatch DXIL on the
hardware adapter, including NaN, infinity, large turns and signed zero.
