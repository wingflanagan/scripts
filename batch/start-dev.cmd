@echo off
setlocal

rem Resolve vmrun path (prefer x86, fallback to 64-bit Program Files)
set "VMRUN=%ProgramFiles(x86)%\VMware\VMware Workstation\vmrun.exe"
if not exist "%VMRUN%" set "VMRUN=%ProgramFiles%\VMware\VMware Workstation\vmrun.exe"

set "VMX=C:\Users\John Flanagan\uwmc-dev_vm\uwmc-dev.vmx"

"%VMRUN%" -T ws start "%VMX%" nogui

rem Capture guest IP address (robust against spaces by redirecting to a file)
set "TMP_IP=%TEMP%\vmrun_guest_ip.txt"
del /q "%TMP_IP%" 2>nul
"%VMRUN%" -T ws getGuestIPAddress "%VMX%" -wait > "%TMP_IP%" 2>nul
set /p GUEST_IP=<"%TMP_IP%"
del /q "%TMP_IP%" 2>nul

if not defined GUEST_IP (
  echo Failed to retrieve guest IP address.
  exit /b 1
)

echo Guest IP: %GUEST_IP%

endlocal
