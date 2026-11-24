@echo off
setlocal
cd /d "%~dp0"
if not exist "WCWBackstageAssault_Recompiled.exe" (
  echo ERROR: WCWBackstageAssault_Recompiled.exe not found.
  exit /b 1
)
"WCWBackstageAssault_Recompiled.exe" %* > boot.log 2>&1
exit /b %ERRORLEVEL%
