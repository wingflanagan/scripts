@echo off

setlocal
cd /d %~dp0

if "%~1"=="" goto NOTITLE
if "%~2"=="" goto NOMSG
goto SHOWMSG

:NOTITLE
echo Please provide title and text parameters. Each must be in double quotes if there are spaces.
goto END

:NOMSG
echo Please provide message text as the second parameter. Must be in double quotes if there are spaces.
goto END

:SHOWMSG
powershell -File .\msgbox.ps1 %2 %1 > nul
goto END

:END
endlocal

@echo on