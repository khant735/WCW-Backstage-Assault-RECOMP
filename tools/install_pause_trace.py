"""Instrument verified-format START mask candidates in a disposable build checkout."""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[1] / "generated"
pattern = re.compile(r"(?m)^([ \t]*\{ uint32_t _pgx\d+ = [^\n]*& 0x0008;[^\n]*\n[^\n]*?/\* 0x([0-9A-Fa-f]{8}): 0x[0-9A-Fa-f]{8} \*/)")
header = r'''
#include <stdio.h>
#include <stdlib.h>
static void wcw_pause_candidate(unsigned pc, unsigned value) {
    static int enabled = -1;
    static FILE *log = NULL;
    if (enabled < 0) {
        const char *e = getenv("WCW_PAUSE_TRACE");
        enabled = e && e[0] == '1' && !e[1];
        if (enabled) log = fopen("wcw-pause-trace.csv", "a");
    }
    if (log) {
        fprintf(log, "%08X,%08X\n", pc, value);
        fflush(log);
    }
}
'''
count = 0
for path in sorted(root.glob("SLUS_012.74_full_*.c")):
    source = path.read_text(encoding="utf-8")
    if "wcw_pause_candidate(" in source:
        raise SystemExit(f"Already instrumented: {path}")
    def hook(m):
        global count
        reg = re.search(r"cpu->gpr\[(\d+)\]\s*=\s*cpu->gpr\[\d+\]\s*&", m[1])
        if not reg:
            return m[0]
        count += 1
        return m[0] + f"\n    wcw_pause_candidate(0x{m[2]}u, cpu->gpr[{reg[1]}]);"
    result = pattern.sub(hook, source)
    if result != source:
        path.write_text(header + result, encoding="utf-8")
if not count:
    raise SystemExit("No matching START candidates")
print(f"Instrumented {count} candidate sites")

# L2 is bit 0x0100 in the PSX active-low pad word. These are candidates,
# not confirmed input handlers. Reuse the proven generated-code format.
focus_pattern = re.compile(pattern.pattern.replace("0x0008", "0x0*100"))
focus_header = header.replace("wcw_pause_candidate", "wcw_focus_candidate").replace("WCW_PAUSE_TRACE", "WCW_FOCUS_TRACE").replace("wcw-pause-trace.csv", "wcw-focus-trace.csv").replace("fflush(log);", "/* buffered; flushed on normal process exit */")
focus_count = 0
for path in sorted(root.glob("SLUS_012.74_full_*.c")):
    source = path.read_text(encoding="utf-8")
    def focus_hook(m):
        global focus_count
        reg = re.search(r"cpu->gpr\[(\d+)\]\s*=\s*cpu->gpr\[\d+\]\s*&", m[1])
        if not reg:
            return m[0]
        focus_count += 1
        return m[0] + f"\n    wcw_focus_candidate(0x{m[2]}u, cpu->gpr[{reg[1]}]);"
    result = focus_pattern.sub(focus_hook, source)
    if result != source:
        path.write_text(focus_header + result, encoding="utf-8")
print(f"Instrumented {focus_count} L2 mask candidate sites")
