@echo off
setlocal

if "%~1"=="" (
  echo Usage: %~nx0 ^<guest-ip^>
  exit /b 1
)

set "GUEST_IP=%~1"
set "SSH=ssh"
set "USER=jflana"

set "TUNNELS=-L 1455:localhost:1455 -L 27017:localhost:27017 -L 3000:localhost:3000 -L 8000:localhost:8000 -L 4321:localhost:4321 -L 35729:localhost:35729"

echo Connecting to %USER%@%GUEST_IP% with port forwards...

%SSH% ^
  -o StrictHostKeyChecking=accept-new ^
  -o ExitOnForwardFailure=yes ^
  %TUNNELS% ^
  %USER%@%GUEST_IP%

endlocal
