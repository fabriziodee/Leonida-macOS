#!/bin/bash
# Storage-aware entry point for the existing original synthetic smoke tests.
set -euo pipefail
if [[ $# != 3 ]]; then
    echo "Usage: $0 BOTTLES_DIR BOTTLE_NAME VICTORY_EXE" >&2
    exit 2
fi
script_dir="$(cd "$(dirname "$0")" && pwd -P)"
case "$2" in
    ""|.|..|*/*|*\\*) echo "Expected a bottle name, not a path" >&2; exit 2 ;;
esac
drive="$1/$2/drive_c"
copies=("$3" "$script_dir/../runtime/test/victory_host_probe.cpp"
        "$script_dir/../runtime/test/victory_entry_probe.cpp")
if [[ -n "${VICTORY_GPU_TEST_EXE:-}" ]]; then
    copies+=("$VICTORY_GPU_TEST_EXE")
fi
if [[ -n "${VICTORY_SHADER_TEST_EXE:-}" ]]; then
    copies+=("$VICTORY_SHADER_TEST_EXE")
fi
"${LEONIDA_PYTHON:-python3}" -I "$script_dir/low_storage.py" \
    --reserve-mib "${LEONIDA_STORAGE_RESERVE_MIB:-1024}" -- "$drive" "${copies[@]}"
# The existing runner owns its unique scratch directory and cleanup.
# Do not alter its validation gates, the bottle, SDK, or shared caches here.
exec /bin/bash "$script_dir/run_victory_macos_smoke.sh" "$@"
