@echo off
setlocal

if "%~1"=="" goto NOCOMMONNAME
if "%~2"=="" goto NOFILENAME
goto MAKECERT

:NOCOMMONNAME
echo Please provide the common name of the web domain (i.e. *.domain.com rather than server.domain.com)
goto END

:NOFILENAME
echo Please provide the path and file name for the certificate
goto END

:MAKECERT
powershell makecert.ps1 %1 %2

:END
endlocal
