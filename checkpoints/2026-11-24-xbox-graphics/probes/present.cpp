#include <windows.h>
#include <d3d12.h>
#include <dxgi1_4.h>
#include <wrl/client.h>
#include <cstdio>

using Microsoft::WRL::ComPtr;

static void check(HRESULT hr, const char* stage) {
    if (FAILED(hr)) {
        printf("FAIL %s: 0x%08lx\n", stage, (unsigned long)hr);
        fflush(stdout);
        ExitProcess(1);
    }
}

static LRESULT CALLBACK wndproc(
    HWND hwnd, UINT msg, WPARAM w, LPARAM l) {
    if (msg == WM_DESTROY) {
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(hwnd, msg, w, l);
}

int main() {
    HINSTANCE instance = GetModuleHandleW(nullptr);
    WNDCLASSW wc{};
    wc.lpfnWndProc = wndproc;
    wc.hInstance = instance;
    wc.lpszClassName = L"Leonida3r1Present";

    if (!RegisterClassW(&wc)) return 2;

    HWND hwnd = CreateWindowW(
        wc.lpszClassName,
        L"LEONIDA 3r1 - D3DMetal Present Probe",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT,
        960, 540, nullptr, nullptr, instance, nullptr);

    if (!hwnd) return 3;

    ShowWindow(hwnd, SW_SHOW);
    UpdateWindow(hwnd);

    ComPtr<ID3D12Device> dev;
    check(D3D12CreateDevice(nullptr,
        D3D_FEATURE_LEVEL_11_0,
        IID_PPV_ARGS(dev.GetAddressOf())), "device");

    ComPtr<ID3D12CommandQueue> queue;
    D3D12_COMMAND_QUEUE_DESC q{};
    q.Type = D3D12_COMMAND_LIST_TYPE_DIRECT;
    check(dev->CreateCommandQueue(&q,
        IID_PPV_ARGS(queue.GetAddressOf())), "queue");

    ComPtr<IDXGIFactory4> factory;
    check(CreateDXGIFactory1(
        IID_PPV_ARGS(factory.GetAddressOf())), "factory");

    DXGI_SWAP_CHAIN_DESC1 desc{};
    desc.Width = 960;
    desc.Height = 540;
    desc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    desc.SampleDesc.Count = 1;
    desc.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    desc.BufferCount = 2;
    desc.SwapEffect = DXGI_SWAP_EFFECT_FLIP_DISCARD;

    ComPtr<IDXGISwapChain1> base;
    check(factory->CreateSwapChainForHwnd(
        queue.Get(), hwnd, &desc, nullptr, nullptr,
        base.GetAddressOf()), "swapchain");

    ComPtr<IDXGISwapChain3> swap;
    check(base.As(&swap), "swapchain3");

    puts("SWAPCHAIN: PASS");
    fflush(stdout);

    D3D12_DESCRIPTOR_HEAP_DESC hd{};
    hd.Type = D3D12_DESCRIPTOR_HEAP_TYPE_RTV;
    hd.NumDescriptors = 2;

    ComPtr<ID3D12DescriptorHeap> heap;
    check(dev->CreateDescriptorHeap(&hd,
        IID_PPV_ARGS(heap.GetAddressOf())), "RTV heap");

    ComPtr<ID3D12Resource> buffers[2];
    D3D12_CPU_DESCRIPTOR_HANDLE handles[2];
    UINT stride = dev->GetDescriptorHandleIncrementSize(
        D3D12_DESCRIPTOR_HEAP_TYPE_RTV);

    for (UINT i = 0; i < 2; i++) {
        check(swap->GetBuffer(i,
            IID_PPV_ARGS(buffers[i].GetAddressOf())), "buffer");
        handles[i] = heap->GetCPUDescriptorHandleForHeapStart();
        handles[i].ptr += SIZE_T(i) * stride;
        dev->CreateRenderTargetView(
            buffers[i].Get(), nullptr, handles[i]);
    }

    ComPtr<ID3D12CommandAllocator> alloc;
    ComPtr<ID3D12GraphicsCommandList> list;
    ComPtr<ID3D12Fence> fence;

    check(dev->CreateCommandAllocator(
        D3D12_COMMAND_LIST_TYPE_DIRECT,
        IID_PPV_ARGS(alloc.GetAddressOf())), "allocator");

    check(dev->CreateCommandList(
        0, D3D12_COMMAND_LIST_TYPE_DIRECT,
        alloc.Get(), nullptr,
        IID_PPV_ARGS(list.GetAddressOf())), "command list");

    check(list->Close(), "initial close");
    check(dev->CreateFence(0, D3D12_FENCE_FLAG_NONE,
        IID_PPV_ARGS(fence.GetAddressOf())), "fence");

    HANDLE event = CreateEventW(nullptr, FALSE, FALSE, nullptr);
    if (!event) return 4;

    const float colors[3][4] = {
        {1.f, 0.f, 1.f, 1.f},
        {0.f, 1.f, 0.f, 1.f},
        {0.f, 0.f, 1.f, 1.f}
    };

    for (UINT frame = 0; frame < 180; frame++) {
        MSG msg;
        while (PeekMessageW(&msg, nullptr, 0, 0, PM_REMOVE)) {
            if (msg.message == WM_QUIT) return 5;
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }

        UINT i = swap->GetCurrentBackBufferIndex();

        check(alloc->Reset(), "allocator reset");
        check(list->Reset(alloc.Get(), nullptr), "list reset");

        D3D12_RESOURCE_BARRIER b{};
        b.Type = D3D12_RESOURCE_BARRIER_TYPE_TRANSITION;
        b.Transition.pResource = buffers[i].Get();
        b.Transition.Subresource =
            D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES;
        b.Transition.StateBefore = D3D12_RESOURCE_STATE_PRESENT;
        b.Transition.StateAfter = D3D12_RESOURCE_STATE_RENDER_TARGET;

        list->ResourceBarrier(1, &b);
        list->ClearRenderTargetView(
            handles[i], colors[frame / 60], 0, nullptr);

        b.Transition.StateBefore = D3D12_RESOURCE_STATE_RENDER_TARGET;
        b.Transition.StateAfter = D3D12_RESOURCE_STATE_PRESENT;
        list->ResourceBarrier(1, &b);

        check(list->Close(), "close");

        ID3D12CommandList* lists[] = {list.Get()};
        queue->ExecuteCommandLists(1, lists);

        HRESULT hr = swap->Present(1, 0);
        check(hr, "present");
        if (hr != S_OK) {
            printf("PRESENT STATUS: 0x%08lx\n", (unsigned long)hr);
            fflush(stdout);
            ExitProcess(6);
        }

        check(queue->Signal(fence.Get(), frame + 1), "signal");
        check(fence->SetEventOnCompletion(frame + 1, event),
              "fence event");

        if (WaitForSingleObject(event, 10000) != WAIT_OBJECT_0) {
            puts("FAIL: GPU fence timeout");
            fflush(stdout);
            ExitProcess(7);
        }

        check(dev->GetDeviceRemovedReason(), "device status");

        if ((frame + 1) % 60 == 0) {
            printf("PRESENT: %u/180 frames\n", frame + 1);
            fflush(stdout);
        }

        Sleep(40);
    }

    CloseHandle(event);
    puts("LEONIDA 3r1 PRESENT: PASS (180/180 frames)");
    return 0;
}
