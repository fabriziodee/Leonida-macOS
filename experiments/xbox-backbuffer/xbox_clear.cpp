#include <windows.h>

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

    // Extended descriptor-heap description includes the zeroed placement.
    struct ExtendedHeap { UINT kind,count,flags,nodes; UINT64 address,size; };
    const ExtendedHeap desc={2,1,0,0,0,0};
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

    using Clear=void(WINAPI*)(Obj,UINT64,const float*,UINT,const RECT*);
    using Close=HRESULT(WINAPI*)(Obj);
    using Reset=HRESULT(WINAPI*)(Obj,Obj,Obj);
    using Execute=void(WINAPI*)(Obj,UINT,const Obj*);
    using Present=HRESULT(WINAPI*)(Obj,UINT,const Plane*,const void*);
    const float colors[3][4]={{1,0,0,1},{0,1,0,1},{0,0,1,1}};
    const float white[4]={1,1,1,1};
    const RECT middle={80,48,240,144};
    Plane plane={1,1,&image};

    for(UINT frame=0;frame<3;frame++) {
        if(frame && method<Reset>(list,0x50)(list,allocator,nullptr)!=0)
            return 17;
        method<Clear>(list,0x1a0)(list,rtv,colors[frame],0,nullptr);
        method<Clear>(list,0x1a0)(list,rtv,white,1,&middle);
        if(method<Close>(list,0x48)(list)!=0) return 18;
        method<Execute>(queue,0x50)(queue,1,&list);
        plane.token=frame+1;
        if(method<Present>(queue,0x100)(queue,1,&plane,nullptr)!=0)
            return 19;
        Sleep(500);
    }
    SAY("XBOX GPU CLEAR: 3 FRAMES SUBMITTED\r\n");
    return 42;
}
