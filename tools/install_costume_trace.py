import pathlib,re,sys
root=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parents[1]/'generated'
p=root/'overlays_static_0001.c'
s=p.read_text(encoding='utf-8')
header=r'''
#include <stdio.h>
#include <stdlib.h>
static void wcw_costume_trace(CPUState *cpu, unsigned pc) {
    static int enabled=-1;
    static FILE *log=NULL;
    static unsigned long long seq=0;
    if (enabled<0) {
        const char *e=getenv("WCW_COSTUME_TRACE");
        enabled=e && e[0]=='1' && !e[1];
        if(enabled) log=fopen("wcw-costume-trace.csv","w");
        if(log) fputs("seq,pc,a0,a1,a2,a3,v0,ra,sp,s0,archive_number,filename\n",log);
    }
    if(!log) return;
    char filename[32]={0};
    int number=-1;
    if(pc==0x800E90F4u) number=(cpu->gpr[4]&255u)*10+(cpu->gpr[5]&255u);
    if(pc==0x800E9180u) {
        number=(int)cpu->gpr[16];
        if(cpu->read_byte) {
            unsigned addr=cpu->gpr[4];
            unsigned phys=addr&0x1fffffffu;
            if(phys<=0x7fffe0u) for(unsigned i=0;i<31;i++) {
                unsigned c=cpu->read_byte(addr+i);
                if(!c) break;
                if(c<32 || c>126 || c==',' || c=='"') { filename[0]=0; break; }
                filename[i]=(char)c;
            }
        }
    }
    fprintf(log,"%llu,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%08X,%d,%s\n",++seq,pc,(unsigned)cpu->gpr[4],(unsigned)cpu->gpr[5],(unsigned)cpu->gpr[6],(unsigned)cpu->gpr[7],(unsigned)cpu->gpr[2],(unsigned)cpu->gpr[31],(unsigned)cpu->gpr[29],(unsigned)cpu->gpr[16],number,filename);
    fflush(log);
}
'''
if 'wcw_costume_trace(' in s: raise SystemExit('Already instrumented')
inc='#include "psx_runtime.h"'
assert s.count(inc)==1
for addr in ('800C2690','800C29B8','800C26A4','800ED624','800E90F4','800E9140','800E9180','800E918C','800E91D0'):
    pattern=rf'(    if \(psx_slice_block\(cpu, 0x{addr}u, [^\n]+\)\) return;\n#endif\n)'
    s,n=re.subn(pattern,lambda m:m[0]+f'    wcw_costume_trace(cpu, 0x{addr}u);\n',s)
    if n!=1: raise SystemExit(f'{addr}: expected one site, found {n}')
    print(addr,n)
p.write_text(s.replace(inc,inc+'\n'+header),encoding='utf-8')
