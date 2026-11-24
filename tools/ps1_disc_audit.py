#!/usr/bin/env python3
"""Read-only PS1 BIN/CUE ISO9660 disc audit for WCW Backstage Assault research.
Supports standard 2352-byte raw Mode 1 or Mode 2 Form 1 sectors and 2048-byte ISO.
No game binaries or proprietary data are redistributed by this script.
"""
import argparse, hashlib, json, pathlib, re, struct, collections

def cue_track(cue):
    s=pathlib.Path(cue).read_text(errors='replace'); files=re.findall(r'^\s*FILE\s+(?:"([^"]+)"|(\S+))\s+BINARY\s*$',s,re.I|re.M)
    if not files: raise ValueError('CUE has no BINARY FILE entry')
    name=files[0][0] or files[0][1]; return pathlib.Path(cue).parent/name

class Disc:
    def __init__(self,path):
        self.path=pathlib.Path(path)
        if self.path.suffix.lower()=='.cue': self.path=cue_track(path)
        if not self.path.is_file(): raise FileNotFoundError(self.path)
        self.fd=self.path.open('rb'); self.size=self.path.stat().st_size
        self.sector_size=self._sector_size()
    def _sector_size(self):
        for size,offset in ((2352,24),(2352,16),(2048,0)):
            if self.size >= (17*size) and (self.size%size==0):
                self.fd.seek(16*size+offset); sec=self.fd.read(2048)
                if sec[1:6]==b'CD001': self.payload_offset=offset; return size
        raise ValueError('Cannot locate ISO9660 Primary Volume Descriptor (first track or Mode 2 Form 2/mixed track not supported)')
    def read_sector(self,lba):
        if lba<0 or (lba+1)*self.sector_size>self.size: raise ValueError('sector outside image')
        self.fd.seek(lba*self.sector_size+self.payload_offset); return self.fd.read(2048)
    def read_extent(self,lba,size):
        if size>512*1024*1024: raise ValueError('oversized extent')
        return b''.join(self.read_sector(lba+i) for i in range((size+2047)//2048))[:size]
    def directory(self,lba,size):
        data=self.read_extent(lba,size); pos=0
        while pos<len(data):
            length=data[pos]
            if not length:
                pos=(pos//2048+1)*2048; continue
            r=data[pos:pos+length]; pos+=length
            if len(r)<34: continue
            n=r[32]; name=r[33:33+n].decode('ascii','replace')
            if name in ('\x00','\x01'):continue
            yield {'name':name,'lba':struct.unpack_from('<I',r,2)[0],'size':struct.unpack_from('<I',r,10)[0], 'directory':bool(r[25]&2)}
    def tree(self):
        pvd=self.read_sector(16)
        if pvd[1:6]!=b'CD001': raise ValueError('ISO9660 not found')
        root=pvd[156:190]; stack=[('',struct.unpack_from('<I',root,2)[0],struct.unpack_from('<I',root,10)[0],0)]
        seen=set(); out=[]
        while stack:
            prefix,lba,size,depth=stack.pop()
            if depth>16 or (lba,size) in seen:continue
            seen.add((lba,size))
            for e in self.directory(lba,size):
                e['path']=prefix+e['name'];out.append(e)
                if e['directory']:stack.append((e['path']+'/',e['lba'],e['size'],depth+1))
        return sorted(out,key=lambda x:x['path'])

def run(paths,out):
    result=[]
    for path in paths:
        disc=Disc(path)
        entries=disc.tree(); types=collections.Counter(pathlib.PurePosixPath(e['path'].split(';')[0]).suffix.upper() or '[none]' for e in entries if not e['directory'])
        system=next((e for e in entries if e['path'].upper().startswith('SYSTEM.CNF')),None)
        sys_txt=disc.read_extent(system['lba'],system['size']).decode('ascii','replace') if system else ''
        boot=re.search(r'BOOT\s*=\s*cdrom:\\?([^\r\n]+)',sys_txt,re.I)
        boot_path=boot.group(1).strip().lstrip('\\/') if boot else None
        exe=next((e for e in entries if boot_path and e['path'].upper()==boot_path.upper()),None)
        executable={'path':exe['path'],'size':exe['size'],'sha256':hashlib.sha256(disc.read_extent(exe['lba'],exe['size'])).hexdigest()} if exe else None
        result.append({'image':str(disc.path),'image_bytes':disc.size,'sector_bytes':disc.sector_size,'system_cnf':sys_txt,'boot_path':boot_path,'boot_executable':executable,'extension_counts':dict(types.most_common()),'files':entries})
        disc.fd.close()
    pathlib.Path(out).write_text(json.dumps(result,indent=2),encoding='utf-8')
    for r in result: print(r['image'],'->',r['boot_path'],'|',len(r['files']),'entries','|',r['extension_counts'])
    if len(result)>1:
        signatures=[]
        for r in result: signatures.append({(f['path'].rsplit('/',1)[-1].split(';')[0].split('.')[-1].upper(),f['size']) for f in r['files'] if not f['directory']})
        print('Shared extension/size tuples:',len(set.intersection(*signatures)))
    print('Wrote',out)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('discs',nargs='+',help='Owned .cue/.bin or .iso images');p.add_argument('--out',default='audit.json'); a=p.parse_args();run(a.discs,a.out)
