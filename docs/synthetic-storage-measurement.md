# Synthetic storage measurement

This read-only sampler complements the proposed low-storage preflight in PR #19,
without requiring that PR to merge first. Use only original synthetic developer
commands and trusted locally built tools. No proprietary content is required.

From the repository root:

```sh
python3 -I scripts/measure_storage.py --workspace /path/to/existing/workspace -- python3 -c 'print("synthetic")'
```

Choose the actual destination volume for the synthetic build or smoke test.
The wrapper launches the specified command without a shell, leaves its output
untouched and emits a single STORAGE_REPORT JSON line to stderr at completion.
The child exit code is preserved when all samples succeed; a measurement
failure is reported explicitly with exit 2.

For a controlled comparison use the same trusted source revision, build
configuration, SDK, and destination filesystem. Compare an empty dedicated
build target with a second run reusing that target. Record the starting
and ending free bytes, minimum sampled free bytes, duration, sample count,
and child exit code. Do not remove existing caches or files automatically.

The maximum sampled free-space drop is a volume-wide estimate, not exclusive
process attribution, an exact peak, a quota, or a guarantee of required space.
Other processes and filesystem snapshots can affect the result; short spikes
may occur between samples. This tool does not measure other destination
volumes or the actual disk footprint of the game. Do not infer savings
without comparable physical Apple Silicon results.

Run the original synthetic unit tests with:

```sh
python3 -I tests/test_measure_storage.py -v
```
