# Indexed Xbox geometry (experimental)

Reuse the verified synthetic RDNA2 VS/PS and the exact diagnostics binary. New 16-bit index buffer, nonzero firstIndex and baseVertex select alternating left/right quads composed of two triangles. A sentinel vertex and degenerate prefix indices distinguish the intended path from incorrectly ignored offsets. Black clear, magenta geometry. Four final frames require all 61,440 sampled RGB pixels (inside and outside both quads) and exact 8/8 host draw counters. No game data, no SDK, no runtime rebuild. Run `bash experiments/xbox-indexed/run.sh` on the original Mac. Reported local M1 Max run passed: 8/8 indexed draws, 8/8 DXGI presentations, expected title exit 42, and 61,440/61,440 sampled RGB pixels matched in frames 5–8. Depth ordering and texture sampling are separate later gates.

## Reported local result · 24 November 2026

```text
Host indexed draws: 8/8 verified
indexed: frame 5: 15360/15360 RGB pixels matched
indexed: frame 6: 15360/15360 RGB pixels matched
indexed: frame 7: 15360/15360 RGB pixels matched
indexed: frame 8: 15360/15360 RGB pixels matched
LEONIDA INDEXED GEOMETRY: PASS (61440 sampled RGB pixels; host draws verified)
```

Run at `c36dae6b`, with the previously verified diagnostics runtime; both synthetic shaders translated. Captures remain local. This verifies the tested index/vertex offsets and alternating geometry, not game execution or general compatibility.
