#!/usr/bin/env python3
"""Original synthetic RDNA2 shaders; format follows VIctory native.rs/dxbc.rs."""
import struct, zlib, pathlib, sys
def pack(fmt,*v): return struct.pack("<"+fmt,*v)
def put(buf,offset,fmt,*v): struct.pack_into("<"+fmt,buf,offset,*v)
def sigs(entries,output=False):
    rows=b""
    names=b""
    for name,system,row,mask in entries:
        at=8+32*len(entries)+len(names)
        rows+=pack("6I4BI",0,at,0,system,3,row,mask,0 if output else mask,0,0,0)
        names+=name.encode()+b"\0"
    return pack("II",len(entries),8)+rows+names
def sig(name,system,output=False):
    return sigs([(name,system,0,15)],output)
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
        data[0x29:0x2e]=bytes((6,1,3,8,1))
        put(data,0xc4,"I",2)
        data[0xc8:0xce]=bytes((6,1,0,0,0,0))
        put(data,0x188,"I",1)
    else:
        data[0x24:0x2c]=bytes((6,1,3,0,0,1,0,0))
        put(data,0x124,"I",1)
        put(data,0x134,"I",2)
    put(record,0,"QQ",len(payload)+len(record)+len(data),len(code))
    put(record,0x14,"I",32 if stage=="ps" else 0)
    put(record,0x50,"I",28|(31<<20))
    tables=b""
    if stage=="ps":
        # Two descriptor tables: sampler in s8/root 1, SRV in s9/root 0.
        # Entries use the native parser's 20-byte layout.
        layout=pack("IIIIBBxx",3,0,1,0,8,1)+pack("IIIIBBxx",3,0,1,0,9,0)
        used=pack("BBxxIIIBBBx",1,3,0,0,0,4,8,1)+pack("BBxxIIIBBBx",0,3,0,0,0,8,9,0)
        at=len(payload)+len(record)+len(data)+len(code)
        put(record,0x28,"QQ",at,at+len(layout))
        put(record,0x38,"II",2,2)
        tables=layout+used
    payload+=record+data+code+tables
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
vs=container([(b"ISG1",sigs([("POSITION",0,0,15),("TEXCOORD",0,1,3)])),
              (b"OSG1",sigs([("SV_Position",1,0,15),("TEXCOORD",0,1,3)],True)),
              (b"DXIL",native("vs",[0xf80000cf,0x07060504,0xf8000a03,0x00000908,0xbf810000]))])
# Native texture lookup from two descriptor tables, explicit LOD zero.
# Perspective-center interpolation of TEXCOORD.xy; sampled RGBA to MRT0.
ps=container([(b"ISG1",sigs([("TEXCOORD",0,1,3)])),(b"OSG1",sig("SV_Target",64,True)),
              (b"DXIL",native("ps",[
                  0xBE820309,0xBE890380,0xBE830380,
                  0xF4080204,0xFA000000,
                  0xF40C0001,0xFA000000,
                  0xBF8CC07F, # wait for scalar loads
                  0xC8080000,0xC8090001,0xC80C0100,0xC80D0101,
                  0xF09C0F08,0x00400002,
                  0xBF8C3F70,0xF800180F,0x03020100,0xBF810000
              ]))])
out=pathlib.Path(sys.argv[1])
out.write_text("\n".join("static const unsigned char "+n+"[] = {"+",".join(str(x) for x in b)+"};" for n,b in [("vs_bytes",vs),("ps_bytes",ps)])+"\n")
print("Original synthetic VS/PS containers generated")
