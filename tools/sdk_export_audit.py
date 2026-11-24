#!/usr/bin/env python3
"""Local, static candidate-export audit. Never loads or executes a title or DLL."""
import argparse
import pathlib
import re
import subprocess
import sys

def read_census(text):
    clean = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    totals = re.findall(r"(?m)^\s*TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$", clean)
    if len(totals) != 1:
        raise ValueError("expected one complete census TOTAL row")
    total, hle, host, missing = map(int, totals[0])
    if total != hle + host + missing:
        raise ValueError("inconsistent census counts")
    pairs = set()
    for dll, name in re.findall(r"(?m)^\s*\d+\s+([^!\s]+\.dll)!(\S+)\s*$", clean, re.I):
        pairs.add((dll.lower(), name))
    if len(pairs) != missing:
        raise ValueError("incomplete missing-symbol list; run census --missing")
    return total, hle, host, pairs

def definition_names(text):
    active = False
    names = set()
    for line in text.splitlines():
        line = line.split(";", 1)[0].strip()
        if not line:
            continue
        if line.upper() == "EXPORTS":
            active = True
            continue
        if not active:
            continue
        if line.split()[0].upper() in {"LIBRARY", "SECTIONS", "IMPORTS", "DESCRIPTION", "STACKSIZE", "HEAPSIZE"}:
            break
        if "NONAME" not in line.upper().split():
            names.add(line.split()[0].split("=")[0])
    return names

def binary_names(text):
    if not re.search(r"(?m)^\s*Format:\s*COFF-x86-64\s*$", text) or "IMAGE_FILE_DLL" not in text:
        raise ValueError("provider is not an x86-64 PE DLL")
    names = set()
    for block in re.findall(r"(?ms)^\s*Export\s*\{(.*?)^\s*\}", text):
        name = re.search(r"(?m)^\s*Name:\s*(\S+)\s*$", block)
        if name:
            names.add(name.group(1))
    return names

def providers(args, binary=False, llvm=None):
    result = {}
    for item in args:
        dll, sep, path = item.partition("=")
        if not sep or not dll.lower().endswith(".dll") or not path:
            raise ValueError("provider must be DLL=PATH")
        key = dll.lower()
        if key in result:
            raise ValueError("duplicate provider")
        if binary:
            out = subprocess.run([llvm, "--file-headers", "--coff-exports", str(pathlib.Path(path).resolve())],
                                 check=True, text=True, stdout=subprocess.PIPE).stdout
            result[key] = binary_names(out)
        else:
            result[key] = definition_names(pathlib.Path(path).read_text(encoding="utf-8-sig"))
    return result

def audit(total, hle, host, missing, definitions, binaries):
    rows = []
    for dll in sorted({d for d, _ in missing}):
        need = {n for d,n in missing if d == dll}
        decl = need & definitions.get(dll, set())
        exported = need & binaries.get(dll, set())
        rows.append((dll, len(need), len(decl), len(exported)))
    return rows

def self_test():
    log = "TOTAL 5 1 1 3\n  1 demo.dll!Read\n  1 demo.dll!Write\n  1 other.dll!Open\n"
    total, hle, host, missing = read_census(log)
    assert (total,hle,host,len(missing)) == (5,1,1,3)
    d = definition_names("LIBRARY demo\nEXPORTS\n Read ; comment\n Write=Impl @2\n Hidden @3 NONAME\n")
    assert d == {"Read","Write"}
    b = binary_names("Format: COFF-x86-64\nIMAGE_FILE_DLL\nExport {\n Ordinal: 1\n Name: Read\n RVA: 0x1000\n}\n")
    assert b == {"Read"}
    assert audit(total,hle,host,missing,{"demo.dll":d},{"demo.dll":b}) == [
        ("demo.dll",2,2,1),("other.dll",1,0,0)]
    for bad in (log.replace("5 1 1 3","6 1 1 3"), log.replace("  1 other.dll!Open\n","")):
        try:
            read_census(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid census accepted")
    try:
        binary_names("Format: COFF-ARM64\nIMAGE_FILE_DLL\n")
    except ValueError:
        pass
    else:
        raise AssertionError("wrong architecture accepted")
    print("SDK audit self-test: PASS (synthetic parser and candidate coverage fixtures)")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--census",type=pathlib.Path)
    p.add_argument("--definition",action="append",default=[],metavar="DLL=DEF")
    p.add_argument("--provider",action="append",default=[],metavar="DLL=PE")
    p.add_argument("--llvm",default="llvm-readobj")
    a=p.parse_args()
    if a.self_test:
        self_test()
        return
    if not a.census:
        p.error("--census or --self-test required")
    total,hle,host,missing=read_census(a.census.read_text(encoding="utf-8-sig"))
    defs=providers(a.definition)
    bins=providers(a.provider,True,a.llvm)
    rows=audit(total,hle,host,missing,defs,bins)
    print(f"Runtime census: {hle+host}/{total} classified (HLE={hle}, host-policy={host}); missing={len(missing)}")
    print(f"{'DLL':45} {'Missing':>8} {'Declared':>9} {'Exported':>9}")
    for dll,n,d,b in rows:
        print(f"{dll:45} {n:8d} {d:9d} {b:9d}")
    print(f"Candidate definitions: {sum(x[2] for x in rows)}/{len(missing)}")
    print(f"Candidate binary exports: {sum(x[3] for x in rows)}/{len(missing)}")
    print("Candidate counts do not change runtime coverage. ABI, dependencies and behavior need separate tests.")

if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"SDK audit: {exc}")
