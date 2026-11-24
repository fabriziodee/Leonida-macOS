#!/usr/bin/env python3
"""Check the exact RGB samples from VIctory's half-resolution back-buffer PNGs."""
import pathlib
import struct
import sys
import zlib

W, H = 160, 96
SIG = b"\x89PNG\r\n\x1a\n"

def require(ok, message):
    if not ok:
        raise ValueError(message)

def decode(data):
    require(data.startswith(SIG), "bad PNG signature")
    pos, header, packed, ended = 8, None, bytearray(), False
    while pos + 12 <= len(data):
        n, kind = struct.unpack_from(">I4s", data, pos)
        require(pos + n + 12 <= len(data), "truncated PNG")
        raw = data[pos+8:pos+8+n]
        crc = struct.unpack_from(">I", data, pos+8+n)[0]
        require(zlib.crc32(kind + raw) == crc, "PNG CRC mismatch")
        pos += n + 12
        if kind == b"IHDR":
            require(header is None and len(raw) == 13, "bad IHDR")
            header = struct.unpack(">IIBBBBB", raw)
        elif kind == b"IDAT":
            packed.extend(raw)
        elif kind == b"IEND":
            require(n == 0, "bad IEND")
            ended = True
            break
    require(ended and pos == len(data), "missing IEND or trailing bytes")
    require(header == (W,H,8,2,0,0,0), f"unexpected PNG format: {header}")
    rows = zlib.decompress(packed)
    stride = 1 + W * 3
    require(len(rows) == stride * H, "wrong decompressed size")
    require(all(rows[y*stride] == 0 for y in range(H)), "unexpected PNG filter")
    return b"".join(rows[y*stride+1:(y+1)*stride] for y in range(H))

def expected(mode, frame):
    result = bytearray()
    for y in range(H):
        for x in range(W):
            if mode == "copy":
                rgb = (255 if x < 80 else 0, 0 if y < 48 else 255,
                       255 if x >= 80 else 0)
            elif 40 <= x < 120 and 24 <= y < 72:
                rgb = (255,255,255)
            else:
                rgb = tuple(255 if c == frame-1 else 0 for c in range(3))
            result.extend(rgb)
    return bytes(result)

def verify(data, mode, frame):
    actual, want = decode(data), expected(mode, frame)
    if actual != want:
        i = next(i for i in range(W*H) if actual[i*3:i*3+3] != want[i*3:i*3+3])
        raise ValueError(f"{mode} frame {frame}: mismatch at ({i%W},{i//W}) "
                         f"got {tuple(actual[i*3:i*3+3])}, expected {tuple(want[i*3:i*3+3])}")

def png(rgb):
    def chunk(kind, raw):
        return (struct.pack(">I",len(raw)) + kind + raw
                + struct.pack(">I",zlib.crc32(kind+raw)))
    raw = b"".join(b"\0"+rgb[y*W*3:(y+1)*W*3] for y in range(H))
    return (SIG + chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,2,0,0,0))
            + chunk(b"IDAT",zlib.compress(raw)) + chunk(b"IEND",b""))

def self_test():
    for mode in ("copy","clear"):
        for frame in (1,2,3):
            good = expected(mode,frame)
            verify(png(good),mode,frame)
            wrong = bytes([good[0]^255])+good[1:]
            for data in (png(wrong),png(good)[:-3],png(good)[:-1]+b"\xff"):
                try:
                    verify(data,mode,frame)
                except (ValueError,zlib.error,struct.error):
                    pass
                else:
                    raise RuntimeError("negative case accepted")
    print("PNG verifier self-test: PASS (6 positive, 18 negative cases)")

if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--self-test"]:
            self_test()
        else:
            require(len(sys.argv)==3 and sys.argv[1] in ("copy","clear"),
                    "usage: verify.py {copy|clear} CAPTURE_DIR")
            mode, folder = sys.argv[1], pathlib.Path(sys.argv[2])
            for f in (1,2,3):
                verify((folder/f"frame-{f}.png").read_bytes(),mode,f)
                print(f"{mode}: frame {f}: {W*H}/{W*H} RGB pixels matched")
            print(f"{mode}: BACKBUFFER PASS ({3*W*H} RGB pixels)")
    except (ValueError,OSError,zlib.error,struct.error) as e:
        sys.exit(str(e))
