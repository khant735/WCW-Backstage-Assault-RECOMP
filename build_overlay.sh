#!/usr/bin/env bash
set -euo pipefail
# Run from checkpoint root. Set FRAMEWORK and RECOMPILER to absolute paths.
cmake -DOUT="$FRAMEWORK/runtime/include/overlay_codegen_hash.h" -DPSXRECOMP_CODEGEN_HASH_ROOT="$FRAMEWORK" -P "$FRAMEWORK/runtime/hash_codegen.cmake"
python3 "$FRAMEWORK/tools/compile_overlays.py" --static --captures "$PWD/captures.json" --game-toml "$PWD/game.toml" --recompiler "$RECOMPILER" --runtime-include "$FRAMEWORK/runtime/include" --out-dir "$PWD/generated" --jobs 2
