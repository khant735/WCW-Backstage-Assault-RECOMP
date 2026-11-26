@echo off
cd /d "%~dp0"
set WCW_PAD_BIOS_TRACE=1
set WCW_PAD_TRACE=1
> wcw-pad-bios-trace.csv echo function,a0,a1,a2,a3,ra
call Launch.cmd %*
