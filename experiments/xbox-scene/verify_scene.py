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
    expected = {1:(6,6), 2:(6,6), 4:(12,12), 8:(24,24)}
    if rows != expected:
        raise ValueError(f"expected all 48 host draws; got {rows}")
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
from scene import raster
print(f"Host scene draws: {total}/48 verified")
count=0
for n in (5,6,7,8):
    reference=raster(((n-1)>>1)&1,(n-1)%2)
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    tested=sum(p is not None for p in reference)
    foreground=sum(p is not None and p!=(0,0,0) for p in reference)
    if tested<13500 or foreground<1500 or tested-foreground<1500:
        sys.exit(f"FAIL: insufficient reference coverage {tested}, foreground {foreground}")
    bad=[(i,tuple(actual[3*i:3*i+3]),p) for i,p in enumerate(reference)
         if p is not None and tuple(actual[3*i:3*i+3])!=p]
    if bad:
        sys.exit(f"FAIL: frame {n}, {len(bad)} differences, first {bad[:5]}")
    count+=tested
    print(f"scene: frame {n}: {tested}/{tested} reference RGB samples matched; {bb.W*bb.H-tested} boundary samples excluded")
print(f"LEONIDA SCENE: PASS ({count} sampled RGB pixels; host draws verified)")
