from pathlib import Path
import re
p=Path("generated/SLUS_012.74_full_02.c")
s=p.read_text(encoding="utf-8")
marker="/* WCW CAW trace */"
if marker in s:
    print("CAW trace already installed")
    raise SystemExit(0)
helper=r'''
/* WCW CAW trace */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static void wcw_caw_trace(CPUState *cpu, unsigned pc) {
    static int enabled=-1;
    static FILE *f=NULL;
    static unsigned seq=0;
    if(enabled<0) {
        const char *e=getenv("WCW_CAW_TRACE");
        enabled=e && strcmp(e,"1")==0;
        if(enabled) {
            f=fopen("wcw-caw-trace.csv","w");
            if(f) fputs("seq,pc,a0,a1,a2,a3,v0,s0,s1,s2,s3,s4,ra,filename\n",f);
        }
    }
    if(!f) return;
    char name[64]={0};
    if(pc==0x8001A818u || pc==0x8001A844u) {
        unsigned addr=cpu->gpr[18], phys=addr & 0x1fffffffu;
        if(phys>=0x10000u && phys<=0x7fffc0u) {
            unsigned i;
            for(i=0;i<sizeof(name)-1;i++) {
                unsigned c=cpu->read_byte(addr+i);
                if(!c) break;
                if(c<32 || c>126 || c==44 || c==34) {name[0]=0;break;}
                name[i]=(char)c;
            }
        }
    }
    fprintf(f,"%u,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%s\n",
        ++seq,pc,(unsigned)cpu->gpr[4],(unsigned)cpu->gpr[5],(unsigned)cpu->gpr[6],(unsigned)cpu->gpr[7],
        (unsigned)cpu->gpr[2],(unsigned)cpu->gpr[16],(unsigned)cpu->gpr[17],(unsigned)cpu->gpr[18],
        (unsigned)cpu->gpr[19],(unsigned)cpu->gpr[20],(unsigned)cpu->gpr[31],name);
    fflush(f);
}
'''
anchor='#include "SLUS_012.74_decls.h"'
assert s.count(anchor)==1
s=s.replace(anchor,anchor+"\n"+helper,1)
for pc in ("8001A754","8001A818","8001A828","8001A844","8001A854","8001A874"):
    pattern=r"(    if \(psx_slice_block\(cpu, 0x"+pc+r"u, [^\n]+\)\) return;\n#endif\n)"
    s,n=re.subn(pattern,lambda m:m[0]+"    wcw_caw_trace(cpu, 0x"+pc+"u);\n",s)
    if n!=1: raise RuntimeError(f"CAW hook {pc}: {n} matches")
p.write_text(s,encoding="utf-8")
print("CAW trace: 6 hooks installed")
