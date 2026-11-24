import importlib.util, pathlib, re, sys

def counters(log):
    # tracing formats field names with ANSI escapes when color is enabled.
    clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", log)
    rows = {}
    for line in clean.splitlines():
        if "frame presented" not in line:
            continue
        fields = dict(re.findall(r"\b(frame|draws|drawn)=(\d+)\b", line))
        if len(fields) != 3:
            raise ValueError("incomplete frame statistics")
        frame = int(fields["frame"])
        if frame in rows:
            raise ValueError("duplicate frame statistics")
        rows[frame] = (int(fields["draws"]), int(fields["drawn"]))
    return rows

def check_counts(log):
    rows = counters(log)
    expected = {1:(1,1), 2:(1,1), 4:(2,2), 8:(4,4)}
    if rows != expected:
        raise ValueError(f"expected all eight host draws; got {rows}")
    return sum(drawn for _, drawn in rows.values())

spec=importlib.util.spec_from_file_location("backbuffer",sys.argv[1])
bb=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)
root=pathlib.Path(sys.argv[2])
log=(root/"execution.log").read_text()
try:
    total=check_counts(log)
except ValueError as e:
    sys.exit(f"FAIL: {e}")
print(f"Host perspective/filter draws: {total}/8 verified")
palette=[(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
# Capture saves source pixels (2*x, 2*y). D3D samples at pixel centers.
# Screen u=(2*x+.5)/320, v=(2*y+.5)/192.
# Right vertex barycentric weight u/2, w=2; others w=1.
# Corrected U=(u/2)/(1-u/4), V=(v-u/4)/(1-u/4).
# U>=.5 iff u>=.8; V>=.5 iff v>=.5+u/8.
def expected(n):
    shift=n-5
    for y in range(bb.H):
        for x in range(bb.W):
            u=(2*x+.5)/320
            v=(2*y+.5)/192
            yield palette[(int(u>=.8)+2*int(v>=.5+u/8)+shift)%4]
for n in (5,6,7,8):
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    pixels=[tuple(actual[i:i+3]) for i in range(0,len(actual),3)]
    if n<=6:
        want=list(expected(n))
        bad=sum(a!=b for a,b in zip(pixels,want))
    else:
        # Center of four equal-area texels: every RGB channel averages .5.
        # UNORM quantization may be 127 or 128.
        bad=sum(any(c not in (127,128) for c in a) for a in pixels)
    if bad:
        sys.exit(f"FAIL: frame {n}, {bad} differing RGB samples; first pixel {pixels[0]}")
    print(f"perspective/filter: frame {n}: {bb.W*bb.H}/{bb.W*bb.H} RGB samples matched")
print("LEONIDA PERSPECTIVE FILTER: PASS (61440 sampled RGB pixels; host draws verified)")
