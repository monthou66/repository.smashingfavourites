@ECHO OFF

:LOOP
tasklist | find /i "kodi" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  ECHO Kodi is still running
  Timeout /T 2 /Nobreak
  GOTO LOOP
)

:CONTINUE
Timeout /T 2 /Nobreak
START "" "E:\XBMC Stuff\kryptonmess\kodi.exe" -p
