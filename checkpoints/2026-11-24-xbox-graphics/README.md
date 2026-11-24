# Leonida 3r1 - Xbox Graphics Checkpoint

Validated on Apple M1 Max, 32 GB RAM,
macOS, CrossOver and D3DMetal.

## Contents

- Standalone D3D12/DXGI presentation probe.
- Synthetic Xbox D3D12.X Device11 / PresentX probe.
- VIctory presenter and texture transition patches.
- Previous local VIctory shader and texture changes.
- Pending Codex runtime modifications.
- Local validation evidence and binary hashes.

## Reproduction

Use the VIctory macOS fork revision recorded in
upstream-commit.txt.

Apply previous-local-changes.patch first, followed
by host.rs.patch and resource.rs.patch in order.

Build the Windows x64 runtime using Rust 1.98.1,
LLVM, LLD and an xwin Windows SDK.

Use the existing D3DMetal CrossOver configuration
and the instructions in docs/victory-macos.md.

## Results

- Standalone DXGI Present: 180/180.
- Internal VIctory presenter: 3/3.
- Texture readback: 64/64 bytes.
- Xbox synthetic imports: 4/4, zero missing.
- D3D12.X Device11: PASS.
- Integrated PresentX: 3/3 DXGI successes.
- Synthetic title exit: 42.
- Runtime exit: 0.

## Pending work

The local Codex runtime and divergent commit patches
are preserved separately for review before integration.
They are not claimed to have passed CI.

No proprietary game files or executable binaries
are included.

GTA VI boot, game rendering, visible pixel correctness,
menu and gameplay remain unverified.
