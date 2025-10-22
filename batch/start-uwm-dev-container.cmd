@echo off
setlocal

set "IMAGE=uwm-dev"
set "NAME=uwm-dev"

if not "%~1"=="" set "IMAGE=%~1"
if not "%~2"=="" set "NAME=%~2"

set "HOST_HOME=%USERPROFILE%"
set "HOST_CODEX=%USERPROFILE%\.codex"
if not exist "%HOST_CODEX%" mkdir "%HOST_CODEX%" >nul 2>&1

REM Build volume args (Windows path quoting)
set "VOL_HOME=%HOST_HOME%:/mnt/home:rw"
set "VOL_CODEX=%HOST_CODEX%:/home/jflana/.codex:rw"

for /f "tokens=* usebackq" %%N in (`podman ps -a --format "{{.Names}}"`) do (
  if /i "%%N"=="%NAME%" (
    echo Starting existing container "%NAME%" ...
    podman start -ai "%NAME%"
    goto :eof
  )
)

echo Creating and starting container "%NAME%" from image "%IMAGE%" ...
podman run -it ^
  --name "%NAME%" ^
  -p 1455:1455 ^
  -v "%VOL_HOME%" ^
  -v "%VOL_CODEX%" ^
  "%IMAGE%" bash

endlocal
