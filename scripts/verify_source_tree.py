#!/usr/bin/env python3
"""Simple local sanity-check for generated files and patch set."""
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
expected = ['CMakeLists.txt','game.toml','generated/SLUS_012.74_dispatch.c',
 'generated/overlays_static.c','runtime_patches/psxrecomp_runtime__src__main.cpp.patch',
 'runtime_patches/psxrecomp_runtime__src__gpu_gl_renderer.c.patch',
 'runtime_patches/psxrecomp_runtime__src__host_osd.c.patch']
missing=[f for f in expected if not (root/f).is_file()]
print('Generated C:',len(list((root/'generated').glob('*.c'))))
print('Missing:',missing)
sys.exit(bool(missing))
