@echo off
setlocal

if "%~1"=="" goto NOFILENAME
goto IMPORTCERT

:NOFILENAME
echo Please provide the path and file name for the certificate
goto END

:IMPORTCERT
powershell importcert.ps1 %1

:END
endlocal
