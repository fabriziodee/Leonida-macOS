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
    expected = {1:(2,2), 2:(2,2), 4:(4,4), 8:(8,8)}
    if rows != expected:
        raise ValueError(f"expected all sixteen host draws; got {rows}")
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
print(f"Host depth draws: {total}/16 verified")
def expected(n):
    color = {5:(255,0,255),6:(255,0,255),7:(0,0,0),8:(0,255,0)}[n]
    return bytes(color)*(bb.W*bb.H)
for n in (5,6,7,8):
    want=expected(n)
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    if actual!=want:
        mismatches=sum(actual[i:i+3]!=want[i:i+3] for i in range(0,len(want),3))
        sys.exit(f"FAIL: frame {n}, {mismatches} differing RGB pixels")
    print(f"depth: frame {n}: {bb.W*bb.H}/{bb.W*bb.H} RGB pixels matched")
print("LEONIDA DEPTH: PASS (61440 sampled RGB pixels; host draws verified)")
