#include <windows.h>
#include <d3d12.h>
#include <intrin.h>
#include <stdio.h>

int main() {
    int cpu[4];
    __cpuid(cpu, 1);
    const bool avxState = (cpu[2] & (1 << 27)) && (cpu[2] & (1 << 28))
        && (_xgetbv(0) & 6) == 6;
    __cpuidex(cpu, 7, 0);
    const bool avx2 = avxState && (cpu[1] & (1 << 5));
    printf("AVX2=%s\n", avx2 ? "yes" : "no");

    ID3D12Device* device = nullptr;
    const HRESULT create = D3D12CreateDevice(
        nullptr, D3D_FEATURE_LEVEL_11_0, IID_PPV_ARGS(&device));
    printf("D3D12CreateDevice=0x%08lx\n", static_cast<unsigned long>(create));
    if (FAILED(create)) return 1;

    D3D12_FEATURE_DATA_SHADER_MODEL shader{D3D_SHADER_MODEL_6_6};
    const HRESULT shaderResult = device->CheckFeatureSupport(
        D3D12_FEATURE_SHADER_MODEL, &shader, sizeof(shader));
    printf("ShaderModel hr=0x%08lx value=0x%x\n",
        static_cast<unsigned long>(shaderResult), static_cast<unsigned>(shader.HighestShaderModel));

    D3D12_FEATURE_DATA_D3D12_OPTIONS7 options{};
    const HRESULT optionsResult = device->CheckFeatureSupport(
        D3D12_FEATURE_D3D12_OPTIONS7, &options, sizeof(options));
    printf("Options7 hr=0x%08lx meshTier=%u\n",
        static_cast<unsigned long>(optionsResult), static_cast<unsigned>(options.MeshShaderTier));
    device->Release();
    return avx2 && SUCCEEDED(shaderResult) && shader.HighestShaderModel >= D3D_SHADER_MODEL_6_6 ? 0 : 2;
}
