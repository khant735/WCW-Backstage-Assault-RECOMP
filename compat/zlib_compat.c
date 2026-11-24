/*
 * zlib entry points required by psxrecomp/runtime/src/boot_state.c.
 * The pinned framework builds miniz (through libchdr), which exposes mz_*.
 * Forward the three used symbols without introducing a second compressor.
 */
#include "miniz.h"

int uncompress(unsigned char *dest, unsigned long *dest_len,
               const unsigned char *source, unsigned long source_len)
{
    return mz_uncompress(dest, dest_len, source, source_len);
}

unsigned long compressBound(unsigned long source_len)
{
    return mz_compressBound(source_len);
}

int compress2(unsigned char *dest, unsigned long *dest_len,
              const unsigned char *source, unsigned long source_len, int level)
{
    return mz_compress2(dest, dest_len, source, source_len, level);
}
