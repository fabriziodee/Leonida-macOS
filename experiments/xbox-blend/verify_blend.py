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
print(f"Host blend draws: {total}/8 verified")
# UNORM conversion of exactly 0.5 may round to 127 or 128.
# Every other channel and every non-alpha mode must match exactly.
for n in (5,6,7,8):
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    allowed={5:{(r,0,b) for r in (127,128) for b in (127,128)},
             6:{(255,0,255)},7:{(0,0,255)},8:{(255,0,0)}}[n]
    bad=sum(tuple(actual[i:i+3]) not in allowed for i in range(0,len(actual),3))
    if bad:
        sys.exit(f"FAIL: frame {n}, {bad} differing RGB pixels; first pixel {tuple(actual[:3])}")
    print(f"blend: frame {n}: {bb.W*bb.H}/{bb.W*bb.H} RGB pixels within expected values")
print("LEONIDA BLEND: PASS (61440 sampled RGB pixels; host draws verified)")
