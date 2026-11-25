/*
 * Export the zlib ABI names referenced by boot_state.c using vendored miniz.
 * miniz.h defines these names as static inline helpers unless compatibility
 * names are disabled. Disable those names in this translation unit only.
 */
#define MINIZ_NO_ZLIB_COMPATIBLE_NAMES
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
