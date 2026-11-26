"""List candidate START bit tests in recompiled game code; not verified handlers."""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[1]
for path in sorted((root / "generated").glob("*.c")):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    label = ""
    for i, line in enumerate(lines):
        if re.match(r"\s*(?:void\s+\w+\(|(?:L_|label_)?[0-9a-fA-F]{8}:)", line):
            label = line.strip()
        if re.search(r"&\s*\(?\s*(?:0x0*8[uU]?|8[uU]?)\b", line):
            print(f"{path.name}:{i+1}: {label}")
            for n in range(max(0,i-4), min(len(lines),i+5)):
                print(f"  {n+1}: {lines[n]}")
