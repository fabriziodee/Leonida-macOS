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
print(f"Host UV draws: {total}/8 verified")
def expected(n):
    palette=[(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
    shift={5:0,6:1,7:2,8:1}[n]
    return bytes(c for y in range(bb.H) for x in range(bb.W)
                 for c in palette[((x>=bb.W//2)+2*(y>=bb.H//2)+shift)%4])
for n in (5,6,7,8):
    want=expected(n)
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    if actual!=want:
        mismatches=sum(actual[i:i+3]!=want[i:i+3] for i in range(0,len(want),3))
        sys.exit(f"FAIL: frame {n}, {mismatches} differing RGB pixels")
    print(f"uv: frame {n}: {bb.W*bb.H}/{bb.W*bb.H} RGB pixels matched")
print("LEONIDA UV: PASS (61440 sampled RGB pixels; host draws verified)")
