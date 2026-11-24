# Xbox multipass render-to-texture and resource transitions (experimental)

Two offscreen render targets plus separate presentation texture. Clear first to black, second to blue, presentation to red. Draw magenta indexed quad into first; transition to COPY_SOURCE, second to COPY_DEST, copy first to second; transition second to render target, draw green indexed quad in opposite position without clearing; transition and copy second into presentation, then COMMON and PresentX. Alternate left/right positions each frame. Exact 16/16 host draws, eight successful presentations and 61,440 RGB samples across four frames required. Explicit whole-resource barriers test transitions and GPU texture copies across two draw passes; not shader texture sampling or general subresource barrier conformance. Reuse known runtime and original synthetic shaders; no game files. Reported local compilation and hardware validation passed at `9b109704`. Run `bash experiments/xbox-multipass/run.sh`.

## Reported M1 Max result · 24 November 2026

```text
Host multipass draws: 16/16 verified
multipass: frame 5: 15360/15360 RGB pixels matched
multipass: frame 6: 15360/15360 RGB pixels matched
multipass: frame 7: 15360/15360 RGB pixels matched
multipass: frame 8: 15360/15360 RGB pixels matched
LEONIDA MULTIPASS: PASS (61440 sampled RGB pixels; host draws verified)
```

Eight DXGI Present calls succeeded; title exit 42. Both shader pipelines created. Three resources, alternating geometry, whole-resource transitions and GPU-to-GPU copies validated through color readback. Shader texture sampling and general subresource synchronization are not yet verified by this probe. Original captures remain local. No game data or runtime modification.
