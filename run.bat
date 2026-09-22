@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title DRMmaster - one click

echo ==============================================
echo   DRMmaster - Adobe DRM removal (one click)
echo ==============================================
echo.

call :findpython
if defined PY goto :deps

echo Python 3 not found - installing now (one-time, ~1 minute)...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProgressPreference='SilentlyContinue';" ^
  "$u='https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe';" ^
  "$f=Join-Path $env:TEMP 'python-installer.exe';" ^
  "Invoke-WebRequest -Uri $u -OutFile $f;" ^
  "Start-Process -Wait -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1 Include_pip=1' -FilePath $f;" ^
  "Remove-Item $f -ErrorAction SilentlyContinue"

set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"
call :findpython
if not defined PY (
  echo.
  echo Python install failed or was interrupted.
  echo Please install it manually from https://www.python.org and run me again.
  pause
  exit /b 1
)

:deps
"%PY%" -c "import Crypto" >nul 2>nul
if errorlevel 1 (
  echo Installing dependencies (one-time)...
  "%PY%" -m venv .venv
  call ".venv\Scripts\pip.exe" install -q -r requirements.txt
  set "PY=.venv\Scripts\python.exe"
)

echo.
"%PY%" run.py
echo.
pause
exit /b 0

:findpython
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY exit /b 0
"%PY%" -c "import sys" >nul 2>nul || set "PY="
exit /b 0
