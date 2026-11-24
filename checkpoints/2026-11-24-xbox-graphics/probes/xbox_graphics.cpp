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

struct Footprint {
    UINT64 offset;
    UINT format, width, height, depth, pitch;
};

struct Location {
    Obj resource;
    UINT kind;
    Footprint footprint;
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

static const Resource buffer_desc = {
    1,0,245760,1,1,1,0,1,0,1,0
};

static void message(const char* text, DWORD size) {
    DWORD written = 0;
    WriteFile(GetStdHandle(STD_OUTPUT_HANDLE),
              text,size,&written,nullptr);
}

#define SAY(x) message(x,sizeof(x)-1)

extern "C" DWORD WINAPI probe_entry() {
    Obj device=nullptr,queue=nullptr,allocator=nullptr;
    Obj list=nullptr,image=nullptr,source=nullptr;

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
        Obj,const Heap*,UINT,const Resource*,
        UINT,const void*,const GUID*,Obj*);

    auto create=method<CreateResource>(device,0xd8);

    if(create(device,&heap,0,&image_desc,
        0x400,nullptr,&RESOURCE,&image)!=0 || !image)
        return 14;

    if(create(device,&heap,0,&buffer_desc,
        0,nullptr,&RESOURCE,&source)!=0 || !source)
        return 15;

    void* mapped=nullptr;

    using Map = HRESULT(WINAPI*)(
        Obj,UINT,const void*,void**);

    if(method<Map>(source,0x40)(
        source,0,nullptr,&mapped)!=0 || !mapped)
        return 16;

    volatile BYTE* p=static_cast<BYTE*>(mapped);

    for(UINT y=0;y<192;y++) {
        for(UINT x=0;x<320;x++) {
            UINT at=y*1280+x*4;
            p[at]=(x<160)?255:0;
            p[at+1]=(y<96)?0:255;
            p[at+2]=(x>=160)?255:0;
            p[at+3]=255;
        }
    }

    Location to={image,0,{0,28,320,192,1,1280}};
    Location from={source,1,{0,28,320,192,1,1280}};

    using Copy=void(WINAPI*)(
        Obj,const Location*,UINT,UINT,UINT,
        const Location*,const void*);

    method<Copy>(list,0x80)(
        list,&to,0,0,0,&from,nullptr);

    using Close=HRESULT(WINAPI*)(Obj);

    if(method<Close>(list,0x48)(list)!=0)
        return 17;

    using Execute=void(WINAPI*)(Obj,UINT,const Obj*);

    method<Execute>(queue,0x50)(queue,1,&list);

    SAY("XBOX GRAPHICS COMMANDS: SUBMITTED\r\n");

    using Present=HRESULT(WINAPI*)(
        Obj,UINT,const Plane*,const void*);

    Plane plane={1,1,&image};

    for(UINT frame=1;frame<=3;frame++) {
        plane.token=frame;

        if(method<Present>(queue,0x100)(
            queue,1,&plane,nullptr)!=0)
            return 18;

        Sleep(1000);
    }

    SAY("XBOX TITLE PRESENTX: 3 CALLS\r\n");

    return 42;
}
