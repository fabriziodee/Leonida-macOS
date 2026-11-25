# Integrated Xbox textured cube (experimental)

Original cube geometry with six indexed faces, two CPU-projected camera orientations with varying clip w, D32_FLOAT depth, two dynamic quadrant textures, translated RDNA2 VS/PS, 48 host draws and eight Present calls. Forward/reverse face order must produce the same interior RGB values for each view. A separate CPU barycentric, perspective-correct texture and depth reference validates the captured frames; explicitly excludes pixels within 0.75 source pixels of triangle edges, near UV discontinuities or equal-depth ties. Requires at least 13,500 compared pixels and 1,500 foreground/background pixels per frame. Not a game scene, shader-driven camera transform, lighting, blending integration, compute dispatch or performance test. Reuses the known runtime without rebuilding. Passed on Apple Silicon using CrossOver D3DMetal and the pinned VIctory diagnostics build with a warmed cache. See the [25 November run](../../PROGRESS.md#integrated-synthetic-scene-on-d3dmetal--25-november-2026) for counts, RGB coverage and cold-start observations. Run `bash experiments/xbox-scene/run.sh`.

## Reproduce on another Apple Silicon Mac

Use an existing isolated D3DMetal bottle, Homebrew LLVM/LLD, an xwin SDK and a locally built VIctory diagnostics runtime with the back-buffer, draw and Present instrumentation from the preceding checkpoints. No game files are needed. A stock VIctory build does not produce the required capture and draw markers. See [back-buffer evidence](../xbox-backbuffer/README.md) and [graphics checkpoint](../../checkpoints/2026-11-24-xbox-graphics/README.md). The original local paths remain defaults; independent testers should set the following variables to their own paths.

```bash
export LEONIDA_VICTORY_EXE=/absolute/path/to/diagnostics/victory.exe
export CX_BOTTLE_PATH=/absolute/path/to/bottles
export LEONIDA_BOTTLE=TestBottle
export XWIN_DIR=/absolute/path/to/xwin-sdk
export LEONIDA_OUTPUT_DIR="$HOME/Developer"
# For a separate known-source build, set its locally verified SHA-256 explicitly.
# The default remains the original diagnostic binary's pinned SHA-256.
export LEONIDA_RUNTIME_SHA256=YOUR_VERIFIED_RUNTIME_SHA256
bash experiments/xbox-scene/run.sh
```

Report the runtime source revision/patches, hardware and backend, `runtime-sha256.txt`, `leonida-commit.txt`, and sanitized `validation.log`. An alternate binary hash identifies a separate reproduction, not the identical original build. The runner still requires all eight Present successes, synthetic exit 42, all 48 host draws and matching RGB samples for four captures. The CPU-only regression is `python3 tests/test_xbox_scene_reference.py`; its generated PNGs are not hardware evidence.
