@echo off
cd /d "%~dp0"
set "WCW_STRETCH=fill"
set "PSX_FPS_TELEMETRY=1"
call Launch.cmd %*
