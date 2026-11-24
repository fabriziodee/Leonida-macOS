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
