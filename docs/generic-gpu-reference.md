# Generic graphics CPU reference — 25 November 2026

Original synthetic reference implementations for independent graphics interoperability testing. No external code, assets or proprietary inputs. AI-assisted.

Run `python -I tests/test_gpu_reference.py`. Seven unit tests passed in an isolated Linux Python environment before publication.

The RGBA8 reference assumes an opaque destination, straight-alpha source, pixel-center nearest scaling, and round-to-nearest integer UNORM values. It does not model linear filtering, BGRA storage, nonopaque destinations, color-space conversion or GPU scheduling. Compare future synthetic hardware results only when the exact format, sampling and blending conventions agree.

The page copy-back model consumes explicit marked byte intervals. It copies each marked page once, handles partial last pages, and is compared to a full-copy result. Tests exercise missing writes, overlapping ranges and 50 successive deterministic randomized submissions. It does not discover GPU writes, implement synchronization, prove atomic ordering or change a runtime. A lower copied-byte count in a fixture is not evidence of a GPU speedup.

Next hardware gate: compare the same original fixtures on native Windows D3D12 and Apple Silicon, with exact adapter and backend identity, source revision, test-process result, pixel or byte comparison and measured latency. Record skips separately. No new hardware or application execution result is claimed.
