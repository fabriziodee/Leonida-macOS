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
