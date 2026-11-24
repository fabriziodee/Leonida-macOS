import importlib.util, pathlib, re, sys
spec=importlib.util.spec_from_file_location("backbuffer",sys.argv[1])
bb=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)
root=pathlib.Path(sys.argv[2])
log=(root/"execution.log").read_text()
# Queue statistics are aggregated between power-of-two frames. At frame 8
# there must be at least three host draws; distinct frames are checked below.
m=re.search(r"frame presented[^\n]*\bframe=8\b[^\n]*\bdrawn=(\d+)",log)
if not m or int(m.group(1))<3:
    sys.exit("FAIL: fewer than three executed host draws in final interval")
want=bytes((255,0,255))*(bb.W*bb.H)
for n in (6,7,8):
    actual=bb.decode((root/"capture"/f"frame-{n}.png").read_bytes())
    if actual!=want:
        sys.exit(f"FAIL: frame {n}, {sum(actual[i:i+3]!=want[i:i+3] for i in range(0,len(want),3))} differing RGB pixels")
    print(f"draw: frame {n}: {bb.W*bb.H}/{bb.W*bb.H} RGB pixels matched")
print("LEONIDA SYNTHETIC DRAW: PASS (46080 sampled RGB pixels; host draws verified)")
