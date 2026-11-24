#include <windows.h>
#include <d3d12.h>
#include "shaders.h"

// This synthetic executable deliberately links without the MSVC CRT.
extern "C" { int _fltused = 0x9875; }

extern "C" __declspec(dllimport)
HRESULT WINAPI D3D12XboxCreateDevice(
    const void*, const UINT*, const GUID*, void**);

using Obj = void*;

template<typename T>
static T method(Obj obj, unsigned offset) {
    return reinterpret_cast<T>(
        (*reinterpret_cast<void***>(obj))[offset / 8]
    );
}

static const GUID DEVICE = {
    0x5405c344,0xd457,0x444e,
    {0xb4,0xdd,0x23,0x66,0xe4,0x5a,0xee,0x39}
};

static const GUID QUEUE = {
    0x0ec870a6,0x5d7e,0x4c22,
    {0x8c,0xfc,0x5b,0xaa,0xe0,0x76,0x16,0xed}
};

static const GUID ALLOCATOR = {
    0x6102dee4,0xaf59,0x4b09,
    {0xb9,0x99,0xb4,0x4d,0x73,0xf0,0x9b,0x24}
};

static const GUID LIST = {
    0xc3827890,0x4024,0x474c,
    {0x98,0xcf,0x64,0x5b,0x51,0xdc,0x48,0x74}
};

static const GUID RESOURCE = {
    0x696442be,0xa72e,0x4059,
    {0xbc,0x79,0x5b,0x5c,0x98,0x04,0x0f,0xad}
};

struct Heap {
    UINT kind, cpu, pool, creation, visible;
};

struct Resource {
    UINT dimension;
    UINT64 alignment, width;
    UINT height;
    USHORT depth, mips;
    UINT format, samples, quality, layout, flags;
};

struct Plane {
    UINT64 token;
    UINT count;
    const Obj* resources;
};

static_assert(sizeof(Resource) == 56);
static_assert(sizeof(Plane) == 24);

static const UINT version = 0x00020004;
static const UINT qdesc[4] = {0,0,0,0};
static const Heap heap = {1,0,0,0,0};

static const Resource image_desc = {
    3,0,320,192,1,1,28,1,0,0,0
};

static void message(const char* text, DWORD size) {
    DWORD written = 0;
    WriteFile(GetStdHandle(STD_OUTPUT_HANDLE),
              text,size,&written,nullptr);
}

#define SAY(x) message(x,sizeof(x)-1)

extern "C" DWORD WINAPI probe_entry() {
    Obj device=nullptr,queue=nullptr,allocator=nullptr;
    Obj list=nullptr,image=nullptr;

    if (D3D12XboxCreateDevice(
        nullptr,&version,&DEVICE,&device)!=0 || !device)
        return 10;

    SAY("XBOX DEVICE11: PASS\r\n");

    using CreateQueue = HRESULT(WINAPI*)(
        Obj,const UINT*,const GUID*,Obj*);

    if (method<CreateQueue>(device,0x180)(
        device,qdesc,&QUEUE,&queue)!=0 || !queue)
        return 11;

    using CreateAllocator = HRESULT(WINAPI*)(
        Obj,UINT,const GUID*,Obj*);

    if (method<CreateAllocator>(device,0x48)(
        device,0,&ALLOCATOR,&allocator)!=0 || !allocator)
        return 12;

    using CreateList = HRESULT(WINAPI*)(
        Obj,UINT,UINT,Obj,Obj,const GUID*,Obj*);

    if (method<CreateList>(device,0x60)(
        device,0,0,allocator,nullptr,&LIST,&list)!=0 || !list)
        return 13;

    using CreateResource = HRESULT(WINAPI*)(
        Obj,const Heap*,UINT,const Resource*,UINT,const void*,const GUID*,Obj*);
    Resource target_desc = image_desc;
    target_desc.flags = 1; // ALLOW_RENDER_TARGET
    if (method<CreateResource>(device,0xd8)(
        device,&heap,0,&target_desc,4,nullptr,&RESOURCE,&image)!=0 || !image)
        return 14;

    Obj first_target=nullptr,second_target=nullptr;
    if(method<CreateResource>(device,0xd8)(device,&heap,0,&target_desc,4,nullptr,&RESOURCE,&first_target)!=0 || !first_target) return 30;
    if(method<CreateResource>(device,0xd8)(device,&heap,0,&target_desc,4,nullptr,&RESOURCE,&second_target)!=0 || !second_target) return 31;

    // Extended descriptor-heap description includes the zeroed placement.
    struct ExtendedHeap { UINT kind,count,flags,nodes; UINT64 address,size; };
    const ExtendedHeap desc={2,3,0,0,0,0};
    const GUID rtv_iid={0x8efb471d,0x616c,0x4f49,
        {0x90,0xf7,0x12,0x7b,0xb7,0x63,0xfa,0x51}};
    Obj descriptors=nullptr;
    using CreateHeap=HRESULT(WINAPI*)(Obj,const ExtendedHeap*,const GUID*,Obj*);
    if(method<CreateHeap>(device,0x70)(device,&desc,&rtv_iid,&descriptors)!=0 || !descriptors)
        return 15;
    using Handle=UINT64(WINAPI*)(Obj);
    const UINT64 rtv=method<Handle>(descriptors,0x48)(descriptors);
    if(!rtv) return 16;
    using CreateRTV=void(WINAPI*)(Obj,Obj,const void*,UINT64);
    method<CreateRTV>(device,0xa0)(device,image,nullptr,rtv);
    const UINT64 first_rtv=rtv+128,second_rtv=rtv+256;
    method<CreateRTV>(device,0xa0)(device,first_target,nullptr,first_rtv);
    method<CreateRTV>(device,0xa0)(device,second_target,nullptr,second_rtv);

    // Xbox stream subobjects, with the padding required by the parser.
    struct Shader { UINT kind,pad; const void* bytes; SIZE_T size; };
    struct Layout { UINT kind,pad; D3D12_INPUT_LAYOUT_DESC data; };
    struct Raster { UINT kind; D3D12_RASTERIZER_DESC data; };
    struct Depth { UINT kind; D3D12_DEPTH_STENCIL_DESC data; };
    struct Topo { UINT kind,value; };
    struct Formats { UINT kind; DXGI_FORMAT formats[8]; UINT count; };
    struct Stream { Shader vs,ps; Layout layout; Raster raster; Depth depth; Topo topology; Formats formats; };
    static_assert(sizeof(Shader)==24 && sizeof(Layout)==24 && sizeof(Raster)==48 &&
                  sizeof(Depth)==56 && sizeof(Formats)==40 && sizeof(Stream)==224);
    static const D3D12_INPUT_ELEMENT_DESC element={"POSITION",0,DXGI_FORMAT_R32G32B32A32_FLOAT,0,0,D3D12_INPUT_CLASSIFICATION_PER_VERTEX_DATA,0};
    static const D3D12_DEPTH_STENCILOP_DESC keep={D3D12_STENCIL_OP_KEEP,D3D12_STENCIL_OP_KEEP,D3D12_STENCIL_OP_KEEP,D3D12_COMPARISON_FUNC_ALWAYS};
    static const Stream stream={
        {1,0,vs_bytes,sizeof(vs_bytes)}, {2,0,ps_bytes,sizeof(ps_bytes)},
        {12,0,{&element,1}},
        {10,{D3D12_FILL_MODE_SOLID,D3D12_CULL_MODE_NONE,FALSE,0,0,0,TRUE,FALSE,FALSE,0,D3D12_CONSERVATIVE_RASTERIZATION_MODE_OFF}},
        {11,{FALSE,D3D12_DEPTH_WRITE_MASK_ZERO,D3D12_COMPARISON_FUNC_ALWAYS,FALSE,255,255,keep,keep}},
        {14,3}, {15,{DXGI_FORMAT_R8G8B8A8_UNORM},1}
    };
    static const Stream green_stream={
        {1,0,vs_bytes,sizeof(vs_bytes)}, {2,0,ps_green_bytes,sizeof(ps_green_bytes)},
        {12,0,{&element,1}},
        {10,{D3D12_FILL_MODE_SOLID,D3D12_CULL_MODE_NONE,FALSE,0,0,0,TRUE,FALSE,FALSE,0,D3D12_CONSERVATIVE_RASTERIZATION_MODE_OFF}},
        {11,{FALSE,D3D12_DEPTH_WRITE_MASK_ZERO,D3D12_COMPARISON_FUNC_ALWAYS,FALSE,255,255,keep,keep}},
        {14,3}, {15,{DXGI_FORMAT_R8G8B8A8_UNORM},1}
    };
    struct StreamDesc { SIZE_T size; const void* stream; };
    const StreamDesc sd={sizeof(stream),&stream};
    const GUID pipeline_iid={0x765a30f3,0xf624,0x4c6f,{0xa8,0x28,0xac,0xe9,0x48,0x62,0x24,0x45}};
    Obj pso=nullptr;
    using CreateStream=HRESULT(WINAPI*)(Obj,const StreamDesc*,const GUID*,Obj*);
    if(method<CreateStream>(device,0x2b0)(device,&sd,&pipeline_iid,&pso)!=0 || !pso) return 20;
    Obj green=nullptr;
    const StreamDesc green_sd={sizeof(green_stream),&green_stream};
    if(method<CreateStream>(device,0x2b0)(device,&green_sd,&pipeline_iid,&green)!=0 || !green) return 32;
    const Resource vertices_desc={1,0,144,1,1,1,0,1,0,1,0};
    Obj vertices=nullptr;
    if(method<CreateResource>(device,0xd8)(device,&heap,0,&vertices_desc,0,nullptr,&RESOURCE,&vertices)!=0 || !vertices) return 21;
    void* mapped=nullptr;
    using Map=HRESULT(WINAPI*)(Obj,UINT,const void*,void**);
    if(method<Map>(vertices,0x40)(vertices,0,nullptr,&mapped)!=0 || !mapped) return 22;
    // Vertex 0 is a sentinel; baseVertex=1 is required.
    static const float xyzw[]={
        0,0,0,1,
        -.75f,.5f,0,1, -.25f,.5f,0,1, -.75f,-.5f,0,1, -.25f,-.5f,0,1,
        .25f,.5f,0,1, .75f,.5f,0,1, .25f,-.5f,0,1, .75f,-.5f,0,1
    };
    for(UINT i=0;i<36;i++) static_cast<volatile float*>(mapped)[i]=xyzw[i];
    using Address=UINT64(WINAPI*)(Obj);
    const D3D12_VERTEX_BUFFER_VIEW vb={method<Address>(vertices,0x58)(vertices),144,16};
    if(!vb.BufferLocation) return 23;
    // Three deliberately degenerate prefix indices; firstIndex=3 or 9.
    const Resource indices_desc={1,0,30,1,1,1,0,1,0,1,0};
    Obj indices=nullptr;
    if(method<CreateResource>(device,0xd8)(device,&heap,0,&indices_desc,0,nullptr,&RESOURCE,&indices)!=0 || !indices) return 24;
    void* index_map=nullptr;
    if(method<Map>(indices,0x40)(indices,0,nullptr,&index_map)!=0 || !index_map) return 25;
    static const USHORT index_data[]={0,0,0,0,1,2,2,1,3,4,5,6,6,5,7};
    for(UINT i=0;i<15;i++) static_cast<volatile USHORT*>(index_map)[i]=index_data[i];
    const D3D12_INDEX_BUFFER_VIEW ib={method<Address>(indices,0x58)(indices),30,DXGI_FORMAT_R16_UINT};
    if(!ib.BufferLocation) return 26;
    const D3D12_VIEWPORT vp={0,0,320,192,0,1};
    const RECT rect={0,0,320,192};
    using SetPipeline=void(WINAPI*)(Obj,Obj);
    using Topology=void(WINAPI*)(Obj,UINT);
    using Viewport=void(WINAPI*)(Obj,UINT,const D3D12_VIEWPORT*);
    using Scissor=void(WINAPI*)(Obj,UINT,const RECT*);
    using Vertex=void(WINAPI*)(Obj,UINT,UINT,const D3D12_VERTEX_BUFFER_VIEW*);
    using Targets=void(WINAPI*)(Obj,UINT,const UINT64*,BOOL,const UINT64*);
    using Index=void(WINAPI*)(Obj,const D3D12_INDEX_BUFFER_VIEW*);
    using Draw=void(WINAPI*)(Obj,UINT,UINT,UINT,INT,UINT);
    using Clear=void(WINAPI*)(Obj,UINT64,const float*,UINT,const RECT*);
    using Close=HRESULT(WINAPI*)(Obj);
    using Reset=HRESULT(WINAPI*)(Obj,Obj,Obj);
    using Execute=void(WINAPI*)(Obj,UINT,const Obj*);
    using Present=HRESULT(WINAPI*)(Obj,UINT,const Plane*,const void*);
    using Barrier=UINT(WINAPI*)(Obj,UINT,const D3D12_RESOURCE_BARRIER*);
    using Copy=void(WINAPI*)(Obj,Obj,Obj);
    // Whole-resource barriers match the supported Xbox ABI.
    const auto transition=[&](Obj resource,D3D12_RESOURCE_STATES from,D3D12_RESOURCE_STATES to) {
        D3D12_RESOURCE_BARRIER b={};
        b.Type=D3D12_RESOURCE_BARRIER_TYPE_TRANSITION;
        b.Transition.pResource=reinterpret_cast<ID3D12Resource*>(resource);
        b.Transition.Subresource=D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES;
        b.Transition.StateBefore=from;
        b.Transition.StateAfter=to;
        method<Barrier>(list,0xd0)(list,1,&b);
    };
    constexpr auto RT=D3D12_RESOURCE_STATE_RENDER_TARGET;
    constexpr auto SRC=D3D12_RESOURCE_STATE_COPY_SOURCE;
    constexpr auto DST=D3D12_RESOURCE_STATE_COPY_DEST;
    constexpr auto COMMON=D3D12_RESOURCE_STATE_COMMON;
    const float black[4]={0,0,0,1},blue[4]={0,0,1,1},red[4]={1,0,0,1};
    Plane plane={1,1,&image};
    for(UINT frame=0;frame<8;frame++) {
        if(frame && method<Reset>(list,0x50)(list,allocator,nullptr)!=0) return 17;
        if(frame) {
            transition(first_target,SRC,RT);
            transition(second_target,SRC,RT);
            transition(image,COMMON,RT);
        }
        method<Clear>(list,0x1a0)(list,first_rtv,black,0,nullptr);
        method<Clear>(list,0x1a0)(list,second_rtv,blue,0,nullptr);
        method<Clear>(list,0x1a0)(list,rtv,red,0,nullptr);
        method<SetPipeline>(list,0xc8)(list,pso);
        method<Topology>(list,0xa0)(list,4);
        method<Viewport>(list,0xa8)(list,1,&vp);
        method<Scissor>(list,0xb0)(list,1,&rect);
        method<Vertex>(list,0x180)(list,0,1,&vb);
        method<Targets>(list,0x190)(list,1,&first_rtv,FALSE,nullptr);
        method<Index>(list,0x178)(list,&ib);
        method<Draw>(list,0x68)(list,6,1,(frame%2)?9:3,1,0);
        transition(first_target,RT,SRC);
        transition(second_target,RT,DST);
        method<Copy>(list,0x88)(list,second_target,first_target);
        transition(second_target,DST,RT);
        method<Targets>(list,0x190)(list,1,&second_rtv,FALSE,nullptr);
        method<SetPipeline>(list,0xc8)(list,green);
        method<Draw>(list,0x68)(list,6,1,(frame%2)?3:9,1,0);
        transition(second_target,RT,SRC);
        transition(image,RT,DST);
        method<Copy>(list,0x88)(list,image,second_target);
        transition(image,DST,COMMON);
        if(method<Close>(list,0x48)(list)!=0) return 18;
        method<Execute>(queue,0x50)(queue,1,&list);
        plane.token=frame+1;
        if(method<Present>(queue,0x100)(queue,1,&plane,nullptr)!=0) return 19;
        Sleep(500);
    }
    SAY("XBOX MULTIPASS: 8 FRAMES SUBMITTED\r\n");
    return 42;
}
