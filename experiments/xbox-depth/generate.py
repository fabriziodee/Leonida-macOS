#!/usr/bin/env python3
"""Original synthetic RDNA2 shaders; format follows VIctory native.rs/dxbc.rs."""
import struct, zlib, pathlib, sys
def pack(fmt,*v): return struct.pack("<"+fmt,*v)
def put(buf,offset,fmt,*v): struct.pack_into("<"+fmt,buf,offset,*v)
def sig(name,system,output=False):
    return pack("II6I4BI",1,8,0,40,0,system,3,0,15,0 if output else 15,0,0,0)+name.encode()+b"\0"
def native(stage,words):
    code=pack("I"*len(words),*words)
    payload=bytearray(0x68)
    put(payload,0,"Q",6)
    for i in (8,16,24,32,40,48,72,96): put(payload,i,"Q",0xdeadbeefdeadbeef)
    put(payload,40 if stage=="vs" else 48,"Q",len(payload))
    record=bytearray(0x54)
    data=bytearray(0x14c+8*404)
    for i in range(8): put(data,0x14c+i*404,"I",0xffffffff)
    if stage=="vs":
        # POSITION.xyzw from v4-v7, semantic row 0.
        data[0x24:0x29]=bytes((6,0,15,4,3))
        put(data,0xc4,"I",1)
    put(record,0,"QQ",len(payload)+len(record)+len(data),len(code))
    put(record,0x14,"I",32 if stage=="ps" else 0)
    put(record,0x50,"I",28|(31<<20))
    payload+=record+data+code
    fssm=b"FSSM"+pack("IQ",0x101,len(payload))+payload
    compressed=zlib.compress(fssm)
    xbch=b"XBCH"+pack("IQQ",3,len(compressed),len(fssm))+compressed
    return bytes(24)+b"XDAT"+pack("IIIII",1,0x24,0x0d,48,len(xbch))+xbch
def container(parts):
    offset=32+4*len(parts)
    offsets=[]; body=b""
    for tag,data in parts:
        offsets.append(offset+len(body))
        body+=tag+pack("I",len(data))+data
    return b"DXBC"+bytes(16)+pack("HHII",1,0,offset+len(body),len(parts))+pack("I"*len(parts),*offsets)+body
def mov(reg,src): return 0x7e000000|(reg<<17)|(1<<9)|src
vs=container([(b"ISG1",sig("POSITION",0)),(b"OSG1",sig("SV_Position",1,True)),
              (b"DXIL",native("vs",[0xf80008cf,0x07060504,0xbf810000]))])
# v_mov_b32 v0, 1.0; v1, 0; v2/v3, 1.0; exp MRT0, done, vm
ps=container([(b"OSG1",sig("SV_Target",64,True)),
              (b"DXIL",native("ps",[mov(0,242),mov(1,128),mov(2,242),mov(3,242),
                                    0xf800180f,0x03020100,0xbf810000]))])
ps_green=container([(b"OSG1",sig("SV_Target",64,True)),
                    (b"DXIL",native("ps",[mov(0,128),mov(1,242),mov(2,128),mov(3,242),
                                          0xf800180f,0x03020100,0xbf810000]))])
out=pathlib.Path(sys.argv[1])
out.write_text("\n".join("static const unsigned char "+n+"[] = {"+",".join(str(x) for x in b)+"};" for n,b in [("vs_bytes",vs),("ps_bytes",ps),("ps_green_bytes",ps_green)])+"\n")
print("Original synthetic VS/PS containers generated")
