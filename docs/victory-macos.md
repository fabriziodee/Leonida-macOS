# VIctory smoke test on Apple Silicon

Use a dedicated 64-bit CrossOver bottle with D3DMetal selected. The smoke
test checks the x64 host capabilities and the VIctory executable entry path
using two synthetic programs.

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
returned 42. The check was AI-assisted.

Boot and visual verification of GTA VI require an authorized Xbox Series
game directory whose executable, companion DLLs and assets are already
readable. GTA VI boot and menus remain unverified on this setup.
