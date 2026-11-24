# Xbox depth test (experimental)

Original synthetic VS and two constant PS colors (magenta/green). D32_FLOAT depth resource, DSV, depth clear and LESS comparison. Near triangle z=0.25, far z=0.75. Frame 5 draws near then far; 6 draws far then near; both must be magenta. Frame 7 clears depth to zero, both rejected (black). Frame 8 draws green and then magenta at the same far depth, requiring LESS to reject the second (green). Exact 16/16 host draw counters, eight successful Present calls and 61,440 sampled RGB pixels across four captures required. This tests the effect of depth on color output, not direct depth readback. Reuses verified runtime, no game data or SDK. Reported local compilation and hardware validation passed at `27824d08`. Run `bash experiments/xbox-depth/run.sh`.

## Reported M1 Max result · 24 November 2026

```text
Host depth draws: 16/16 verified
depth: frame 5: 15360/15360 RGB pixels matched
depth: frame 6: 15360/15360 RGB pixels matched
depth: frame 7: 15360/15360 RGB pixels matched
depth: frame 8: 15360/15360 RGB pixels matched
LEONIDA DEPTH: PASS (61440 sampled RGB pixels; host draws verified)
```

Two host pipelines created, eight DXGI Present calls succeeded, expected title exit 42. Black-frame warning at frame 7 is intentional (zero depth clear rejects both triangles). Color readback validates the tested LESS, depth-write and clear behavior, not direct depth readback or all depth formats. Original captures remain local; no game data used. Runtime unchanged.
