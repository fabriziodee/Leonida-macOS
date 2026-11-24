# VIctory smoke test on Apple Silicon

Use a dedicated 64-bit CrossOver bottle with D3DMetal selected. The smoke
test checks the x64 host capabilities and the VIctory executable entry path
using two synthetic programs. The host probe also clears a 4x4
RGBA8 render target, copies it to a CPU-readable buffer, waits for a fence
(up to ten seconds), and checks every pixel. This tests actual D3D12 command
execution rather than only reported feature levels; it does not test shaders,
video decoding, presentation or game startup.

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
