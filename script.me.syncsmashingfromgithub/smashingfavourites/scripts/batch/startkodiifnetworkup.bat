@ECHO OFF

rem check if kodi's already running
tasklist | find /i "kodi" >nul 2>&1
rem start kodi when network's up
IF ERRORLEVEL 1 (
  ECHO Kodi is not running
  GOTO CONTINUE
) ELSE (
  ECHO Kodi is already running
  PAUSE
  EXIT
)
:CONTINUE
rem check if internet connected.  If not, wait  / loop
echo checking internet connection
:LOOP
Ping www.google.nl -n 1 -w 1000
cls
IF ERRORLEVEL 1 (
  ECHO No internet detected.
  ECHO Hang on a tick
  Timeout /T 2 /Nobreak
  GOTO LOOP
) ELSE (
  GOTO STARTKODI
)
:STARTKODI
rem START "" "C:\Program Files\Kodi\kodi.exe"

START "" "E:\XBMC Stuff\kryptonsql\kodi.exe" -p
