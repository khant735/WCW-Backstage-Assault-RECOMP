@echo off
setlocal
cd /d "%~dp0"
set "WCW_FMV_LANCZOS=1"
call Launch.cmd %*
exit /b %ERRORLEVEL%
