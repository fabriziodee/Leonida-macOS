#include <windows.h>
#include <d3d12.h>
#include <intrin.h>
#include <stdio.h>

#include <wrl/client.h>
#include <stdint.h>

using Microsoft::WRL::ComPtr;

// Synthetic render-target clear and readback through the host D3D12 driver.
// A successful capability query alone does not establish that GPU work executes.
static bool gpu_readback(ID3D12Device* device) {
    constexpr UINT width = 4, height = 4;
    auto check = [](HRESULT hr, const char* stage) {
        if (FAILED(hr)) {
            printf("GPU readback %s failed: 0x%08lx\n", stage, static_cast<unsigned long>(hr));
            return false;
        }
        return true;
    };

    D3D12_COMMAND_QUEUE_DESC queueDesc{};
    queueDesc.Type = D3D12_COMMAND_LIST_TYPE_DIRECT;
    ComPtr<ID3D12CommandQueue> queue;
    ComPtr<ID3D12CommandAllocator> allocator;
    ComPtr<ID3D12GraphicsCommandList> list;
    ComPtr<ID3D12Fence> fence;
    if (!check(device->CreateCommandQueue(&queueDesc, IID_PPV_ARGS(queue.GetAddressOf())), "queue") ||
        !check(device->CreateCommandAllocator(D3D12_COMMAND_LIST_TYPE_DIRECT,
              IID_PPV_ARGS(allocator.GetAddressOf())), "allocator") ||
        !check(device->CreateCommandList(0, D3D12_COMMAND_LIST_TYPE_DIRECT, allocator.Get(), nullptr,
              IID_PPV_ARGS(list.GetAddressOf())), "list") ||
        !check(device->CreateFence(0, D3D12_FENCE_FLAG_NONE, IID_PPV_ARGS(fence.GetAddressOf())), "fence"))
        return false;

    D3D12_RESOURCE_DESC texture{};
    texture.Dimension = D3D12_RESOURCE_DIMENSION_TEXTURE2D;
    texture.Width = width;
    texture.Height = height;
    texture.DepthOrArraySize = 1;
    texture.MipLevels = 1;
    texture.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    texture.SampleDesc.Count = 1;
    texture.Layout = D3D12_TEXTURE_LAYOUT_UNKNOWN;
    texture.Flags = D3D12_RESOURCE_FLAG_ALLOW_RENDER_TARGET;

    D3D12_HEAP_PROPERTIES gpu{};
    gpu.Type = D3D12_HEAP_TYPE_DEFAULT;
    gpu.CreationNodeMask = gpu.VisibleNodeMask = 1;
    ComPtr<ID3D12Resource> target;
    if (!check(device->CreateCommittedResource(&gpu, D3D12_HEAP_FLAG_NONE, &texture,
            D3D12_RESOURCE_STATE_RENDER_TARGET, nullptr, IID_PPV_ARGS(target.GetAddressOf())), "target"))
        return false;

    D3D12_DESCRIPTOR_HEAP_DESC rtvDesc{};
    rtvDesc.Type = D3D12_DESCRIPTOR_HEAP_TYPE_RTV;
    rtvDesc.NumDescriptors = 1;
    ComPtr<ID3D12DescriptorHeap> rtv;
    if (!check(device->CreateDescriptorHeap(&rtvDesc, IID_PPV_ARGS(rtv.GetAddressOf())), "RTV heap"))
        return false;
    const auto handle = rtv->GetCPUDescriptorHandleForHeapStart();
    device->CreateRenderTargetView(target.Get(), nullptr, handle);

    D3D12_PLACED_SUBRESOURCE_FOOTPRINT footprint{};
    UINT64 bytes = 0;
    device->GetCopyableFootprints(&texture, 0, 1, 0, &footprint, nullptr, nullptr, &bytes);
    if (!bytes || bytes == UINT64_MAX || footprint.Footprint.RowPitch < width * 4 ||
        footprint.Offset > bytes || bytes - footprint.Offset <
            UINT64(height - 1) * footprint.Footprint.RowPitch + width * 4) {
        puts("GPU readback invalid copy footprint");
        return false;
    }

    D3D12_HEAP_PROPERTIES cpu = gpu;
    cpu.Type = D3D12_HEAP_TYPE_READBACK;
    D3D12_RESOURCE_DESC buffer{};
    buffer.Dimension = D3D12_RESOURCE_DIMENSION_BUFFER;
    buffer.Width = bytes;
    buffer.Height = buffer.DepthOrArraySize = buffer.MipLevels = 1;
    buffer.SampleDesc.Count = 1;
    buffer.Layout = D3D12_TEXTURE_LAYOUT_ROW_MAJOR;
    ComPtr<ID3D12Resource> readback;
    if (!check(device->CreateCommittedResource(&cpu, D3D12_HEAP_FLAG_NONE, &buffer,
            D3D12_RESOURCE_STATE_COPY_DEST, nullptr, IID_PPV_ARGS(readback.GetAddressOf())), "readback"))
        return false;

    const float color[] = {1.0f, 0.0f, 1.0f, 1.0f};
    list->ClearRenderTargetView(handle, color, 0, nullptr);
    D3D12_RESOURCE_BARRIER barrier{};
    barrier.Type = D3D12_RESOURCE_BARRIER_TYPE_TRANSITION;
    barrier.Transition.pResource = target.Get();
    barrier.Transition.Subresource = D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES;
    barrier.Transition.StateBefore = D3D12_RESOURCE_STATE_RENDER_TARGET;
    barrier.Transition.StateAfter = D3D12_RESOURCE_STATE_COPY_SOURCE;
    list->ResourceBarrier(1, &barrier);

    D3D12_TEXTURE_COPY_LOCATION src{}, dst{};
    src.pResource = target.Get();
    src.Type = D3D12_TEXTURE_COPY_TYPE_SUBRESOURCE_INDEX;
    dst.pResource = readback.Get();
    dst.Type = D3D12_TEXTURE_COPY_TYPE_PLACED_FOOTPRINT;
    dst.PlacedFootprint = footprint;
    list->CopyTextureRegion(&dst, 0, 0, 0, &src, nullptr);
    if (!check(list->Close(), "close")) return false;
    ID3D12CommandList* lists[] = {list.Get()};
    queue->ExecuteCommandLists(1, lists);
    if (!check(queue->Signal(fence.Get(), 1), "signal")) return false;

    const ULONGLONG start = GetTickCount64();
    for (;;) {
        const UINT64 completed = fence->GetCompletedValue();
        if (completed == UINT64_MAX) {
            check(device->GetDeviceRemovedReason(), "device removed");
            return false;
        }
        if (completed >= 1) break;
        if (GetTickCount64() - start >= 10000) {
            puts("GPU readback fence timed out");
            // Work may still be in flight; terminate the standalone probe rather
            // than releasing its resources before GPU completion.
            fflush(stdout);
            ExitProcess(3);
        }
        Sleep(1);
    }

    void* mapped = nullptr;
    const D3D12_RANGE readRange{0, static_cast<SIZE_T>(bytes)};
    if (!check(readback->Map(0, &readRange, &mapped), "map")) return false;
    if (!mapped) {
        const D3D12_RANGE noWrite{0, 0};
        readback->Unmap(0, &noWrite);
        puts("GPU readback returned a null map");
        return false;
    }
    bool matches = true;
    for (UINT y = 0; y < height; ++y) {
        const auto* row = static_cast<const uint8_t*>(mapped) + footprint.Offset +
                          UINT64(y) * footprint.Footprint.RowPitch;
        for (UINT x = 0; x < width; ++x) {
            const auto* p = row + x * 4;
            if (p[0] != 255 || p[1] != 0 || p[2] != 255 || p[3] != 255) matches = false;
        }
    }
    const D3D12_RANGE noWrite{0, 0};
    readback->Unmap(0, &noWrite);
    printf("GPU clear/readback: %s\n", matches ? "PASS (16 RGBA pixels)" : "FAIL (pixel mismatch)");
    return matches;
}


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
    const bool gpu = gpu_readback(device);
    device->Release();
    if (!gpu) return 3;
    return avx2 && SUCCEEDED(shaderResult) && shader.HighestShaderModel >= D3D_SHADER_MODEL_6_6 ? 0 : 2;
}
