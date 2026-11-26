@echo off
setlocal
cd /d "%~dp0"
set "WCW_LOADING_TRACE=1"
call Launch.cmd %*
exit /b %ERRORLEVEL%
