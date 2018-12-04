@ECHO OFF

set one="E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\test.txt"
set two="E:\XBMC Stuff\kryptonmess\portable_data\userdata\Database\test.txt"

:LOOP
tasklist | find /i "kodi" >nul 2>&1
IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
  ECHO Kodi is still running
  Timeout /T 5 /Nobreak
  GOTO LOOP
)

:CONTINUE

move %one% %two%

Timeout /T 2 /Nobreak

START "" "E:\XBMC Stuff\kryptonmess\kodi.exe" -p