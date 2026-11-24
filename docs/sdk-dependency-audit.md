# Public SDK dependency audit

This local-only tool separates runtime census classifications from public SDK declarations and candidate PE exports. It never maps or executes binaries; it does not claim ABI or behavioral compatibility, infer that host-policy imports resolve at runtime, or add stub successes.

```sh
python3 tools/sdk_export_audit.py --self-test
python3 tools/sdk_export_audit.py --census /path/to/local/census.log \
  --definition example.dll=/path/to/public/exports.def
# Optional, only for a trusted, authorized x86-64 DLL:
python3 tools/sdk_export_audit.py --census /path/to/local/census.log \
  --provider example.dll=/path/to/authorized/example.dll \
  --llvm /opt/homebrew/opt/llvm/bin/llvm-readobj
```

Use VIctory's `census --missing` output locally. Do not commit title-specific census logs, executable fingerprints, binaries, keys or proprietary assets. Candidate symbols are counted once per DLL; a declaration is not an implementation and an export is not a functioning API. Ordinal-only matches are not counted by this name-based tool.

## Public SDK research

- [Microsoft libHttpClient public export definition, pinned c5007fd](https://github.com/microsoft/libHttpClient/blob/c5007fd9cbdc785518ea6dccc5751b125d451cc1/Build/libHttpClient.GDK/libHttpClient.GDK.def). The repository includes a GDK DLL project and public source. Build through the appropriate licensed SDK/toolchain; verify x64 exports, calling conventions, async task queue semantics and offline synthetic HTTP tests before integrating.
- [AMD FidelityFX SDK](https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK) and [public Microsoft GDK sample](https://github.com/microsoft/Xbox-GDK-Samples/tree/main/Samples/Graphics/AMD_FSR). PC and Xbox loader names differ. Matching function names are insufficient; validate descriptors, resource ownership and output through a synthetic dispatch.
- [DirectX Raytracing specification](https://microsoft.github.io/DirectX-Specs/d3d/Raytracing.html). Standard DXR does not establish Xbox-specific builder ABI or acceleration structure compatibility.
- [Bink SDK](https://www.radgametools.com/bnkdown.htm). Use authorized SDK components and test original synthetic media. Do not substitute arbitrary same-named binaries.

Next: compile public components in supported toolchains, compare exports, validate ABI and functional fixtures, then integrate into the runtime. No changes to the loader's protections, import resolver or reported hardware compatibility are made by this audit.

## Local validation and public Windows SDK candidate · 24 November 2026

The original synthetic audit self-test was reported passing on Apple Silicon at `3d5e535`. The public Microsoft export definition was successfully parsed locally. This does not change runtime coverage. For general Windows GDK compatibility development, the official [Microsoft.GDK.Windows 2604.5.7903 package](https://www.nuget.org/packages/Microsoft.GDK.Windows/2604.5.7903) is a candidate source of desktop x64 SDK components, subject to its license. Inspect the package contents and PE exports locally before attempting any synthetic functional tests. The package's actual DLL contents, binary compatibility and behavior have not been verified on the Mac. Keep SDK binaries and title-specific data out of the repository. No actual game boot is claimed.

## Desktop x64 candidate confirmed by static inspection

Reported local extraction of the official Windows GDK NuGet package succeeded. The desktop `libHttpClient.dll` is an x86-64 PE DLL with 129 named exports. The certificate directory is present (signature validity was not independently verified). Candidate export matching succeeded in the reported log analysis. The Windows desktop DLL name differs from the GDK console name; no alias, runtime resolver change or ABI equivalence is asserted. Next gate: an independent Windows x64 synthetic process must load the trusted SDK DLL and exercise its public request creation, configuration, readback and cleanup functions without sending traffic. Keep the SDK binaries local and respect their license.

## Windows GDK / LibHttpClient synthetic smoke test — PASS

Reported Apple Silicon / CrossOver run: V2 initialization failed with `0x89240101`; V3 with the official desktop SDK dependencies present failed with `0x89240100`. V4 linked `xgameruntime.lib`, `advapi32.lib` and `kernel32.lib`, called `XGameRuntimeInitialize` before `HCInitialize`, and reported both HRESULTs as `0x00000000`. The independent synthetic executable completed request-handle creation, URL/method round-trip, timeout round-trip, header count, four-byte request-body round-trip, handle close and cleanup, and exited 42. No request was sent. This establishes a desktop SDK smoke-test milestone, not console ABI compatibility, complete API coverage or game execution. Next functional gate: asynchronous request to a local fixture and verified response status/body using the documented SDK task queue. No runtime import resolver modification or change to the graphics evidence totals.
