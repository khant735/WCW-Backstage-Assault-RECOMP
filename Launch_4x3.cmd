@echo off
cd /d "%~dp0"
set "WCW_STRETCH="
set "PSX_FPS_TELEMETRY=1"
call Launch.cmd %*
