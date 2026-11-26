@echo off
cd /d "%~dp0"
set WCW_FOCUS_TRACE=1
set WCW_PAD_TRACE=1
set WCW_PAUSE_TRACE=0
> wcw-focus-trace.csv echo PC,value
call Launch.cmd
