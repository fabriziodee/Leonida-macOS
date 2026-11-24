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

if sys.argv[1:] == ["--self-test"]:
    plain = "\n".join(f"INFO frame presented frame={f} draws={n} drawn={n}"
                      for f,n in ((1,1),(2,1),(4,2),(8,4)))
    color = re.sub(r"(frame|draws|drawn)=", lambda m: "\x1b[1m"+m[1]+"\x1b[0m=", plain)
    assert check_counts(plain) == check_counts(color) == 8
    for bad in (plain.replace("drawn=4","drawn=0"), plain.rsplit("\n",1)[0]):
        try:
            check_counts(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("accepted invalid counters")
    print("Draw log parser self-test: PASS (2 positive, 2 negative)")
    sys.exit(0)

spec=importlib.util.spec_from_file_location("backbuffer",sys.argv[1])
bb=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)
root=pathlib.Path(sys.argv[2])
log=(root/"execution.log").read_text()
try:
    total=check_counts(log)
except ValueError as e:
    sys.exit(f"FAIL: {e}")
print(f"Host draws: {total}/8 verified")
want=bytes((255,0,255))*(bb.W*bb.H)
for n in (6,7,8):
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    if actual!=want:
        sys.exit(f"FAIL: frame {n}, {sum(actual[i:i+3]!=want[i:i+3] for i in range(0,len(want),3))} differing RGB pixels")
    print(f"draw: frame {n}: {bb.W*bb.H}/{bb.W*bb.H} RGB pixels matched")
print("LEONIDA SYNTHETIC DRAW: PASS (46080 sampled RGB pixels; host draws verified)")
