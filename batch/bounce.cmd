@SETLOCAL
@IF [%1] == [] (
    SET t=0
) ELSE (
    SET t=%1
)

@shutdown /r /t %t%
@ENDLOCAL