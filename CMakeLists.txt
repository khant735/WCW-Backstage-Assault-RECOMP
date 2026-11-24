cmake_minimum_required(VERSION 3.20)
project(WCWBackstageAssault LANGUAGES C CXX)
set(PSXRECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/psxrecomp" CACHE PATH "Framework path")
set(PSX_RECOMP_UI OFF CACHE BOOL "No launcher UI" FORCE)
set(MINIZ_DEFLATE_APIS ON CACHE BOOL "Enable savestate compression" FORCE)
include("${PSXRECOMP_ROOT}/runtime/runtime.cmake")
if(TARGET miniz)
  add_library(wcw_zlib_compat INTERFACE)
  target_link_libraries(wcw_zlib_compat INTERFACE miniz)
  target_include_directories(wcw_zlib_compat INTERFACE "${CMAKE_CURRENT_SOURCE_DIR}/compat" "${FETCHCONTENT_SOURCE_DIR_PSX_LIBCHDR}/deps/miniz-3.1.1")
  add_library(ZLIB::ZLIB ALIAS wcw_zlib_compat)
endif()
psxrecomp_add_game_runtime(psx-runtime
 PRELOADED_MODS_DIR NONE
 WINDOW_TITLE "WCW Backstage Assault Recompiled"
 EXE_NAME "WCWBackstageAssault_Recompiled"
 MAX_PLAYERS 2
 DEFAULT_GAME_CONFIG_PATH "game.toml"
 EXCLUDE_BUILTIN_MODS psx.enhancement.fast-loading
 GAME_OVERLAY_STATIC_C "${CMAKE_CURRENT_SOURCE_DIR}/generated/overlays_static.c"
 GEN_MARKER "generated/SLUS_012.74_dispatch.c"
 GEN_FULL_GLOB "generated/SLUS_012.74_full_*.c")

# The pinned framework compiles miniz through libchdr, but boot_state.c
# references three zlib ABI names. Export the compatible entry points.
if(NOT TARGET miniz)
  message(FATAL_ERROR "Expected vendored miniz target from psx_libchdr")
endif()
target_sources(psx-runtime PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/compat/zlib_compat.c")
target_include_directories(psx-runtime PRIVATE "${FETCHCONTENT_SOURCE_DIR_PSX_LIBCHDR}/deps/miniz-3.1.1")
target_link_libraries(psx-runtime PRIVATE miniz)
