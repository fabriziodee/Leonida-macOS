#!/bin/bash
# Build and run two synthetic probes against an existing VIctory Windows build.
set -euo pipefail

if [[ $# != 3 ]]; then
    echo "Usage: XWIN_DIR=/path/to/sdk $0 BOTTLES_DIR BOTTLE_NAME VICTORY_EXE" >&2
    exit 2
fi

: "${XWIN_DIR:?Set XWIN_DIR to the Windows SDK prepared with xwin}"
wine="${CROSSOVER_WINE:-/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine}"
clang_cl="${CLANG_CL:-/opt/homebrew/opt/llvm/bin/clang-cl}"
lld_dir="${LLD_DIR:-/opt/homebrew/opt/lld/bin}"
export PATH="$lld_dir:$PATH"

export CX_BOTTLE_PATH="$(cd "$1" && pwd -P)"
bottle="$2"
victory="$(cd "$(dirname "$3")" && pwd -P)/$(basename "$3")"
shader_tests=${VICTORY_SHADER_TEST_EXE:-}
if [[ -n "$shader_tests" ]]; then
    shader_tests="$(cd "$(dirname "$shader_tests")" && pwd -P)/$(basename "$shader_tests")"
    [[ -f "$shader_tests" ]]
fi
gpu_tests=${VICTORY_GPU_TEST_EXE:-}
if [[ -n "$gpu_tests" ]]; then
    gpu_tests="$(cd "$(dirname "$gpu_tests")" && pwd -P)/$(basename "$gpu_tests")"
    [[ -f "$gpu_tests" ]]
fi
if [[ "${VICTORY_REQUIRE_EXTENDED:-0}" == 1 && ( -z "$gpu_tests" || -z "$shader_tests" ) ]]; then
    echo "Extended smoke test requires both GPU and shader test executables" >&2
    exit 2
fi
drive="$CX_BOTTLE_PATH/$bottle/drive_c"
[[ -d "$drive" && -f "$victory" && -x "$wine" && -x "$clang_cl" ]]
source_dir="$(cd "$(dirname "$0")/../runtime/test" && pwd -P)"

scratch="$(mktemp -d "$drive/leonida-smoke.XXXXXXXX")"
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
cp "$victory" victory.exe
cp "$source_dir"/victory_{host,entry}_probe.cpp .

"$clang_cl" --target=x86_64-pc-windows-msvc -fuse-ld=lld /winsysroot "$XWIN_DIR" \
    /O2 /MT victory_host_probe.cpp /Fehost-probe.exe /link d3d12.lib
"$clang_cl" --target=x86_64-pc-windows-msvc -fuse-ld=lld /winsysroot "$XWIN_DIR" \
    /O2 /GS- /Zl victory_entry_probe.cpp /Feentry-probe.exe \
    /link /entry:probe_entry /subsystem:console /nodefaultlib kernel32.lib

guest="C:\\${scratch##*/}"
"$wine" --bottle "$bottle" --no-update --cx-app "$guest\\host-probe.exe"
"$wine" --bottle "$bottle" --no-update --cx-app "$guest\\victory.exe" \
    run "$guest\\entry-probe.exe" --execute | tee launch.log
grep -Fq 'VIctory synthetic title entry reached' launch.log
grep -Fq 'title exited with 42' launch.log

if [[ -n "$gpu_tests" ]]; then
    cp "$gpu_tests" gpu-tests.exe
    "$wine" --bottle "$bottle" --no-update --cx-app "$guest\\gpu-tests.exe" \
        --exact resource::tests::buffer_data_reaches_the_host_texture --nocapture 2>&1 | tee texture.log
    grep -Fq 'VIctory texture upload/readback: 64 bytes matched' texture.log
    grep -Fq '1 passed; 0 failed; 0 ignored' texture.log
fi

if [[ -n "$shader_tests" ]]; then
    cp "$shader_tests" shader-tests.exe
    for width in f32 f16; do
        test_name="emit::valu_tests::v_sin_and_v_cos_${width}_reduce_large_turns"
        VICTORY_WARP=0 "$wine" --bottle "$bottle" --no-update --cx-app "$guest\\shader-tests.exe" \
            --exact "$test_name" --nocapture --test-threads=1 2>&1 | tee "shader-$width.log"
        grep -Fq '1 passed; 0 failed; 0 ignored' "shader-$width.log"
        if grep -Eiq 'no SM 6\.6 (hardware|warp) device|(^|[[:space:];])skipped([[:space:][:punct:]]|$)' "shader-$width.log"; then
            echo "The shader fixture was skipped or could not use the hardware adapter; not a verified PASS" >&2
            exit 1
        fi
    done
fi
