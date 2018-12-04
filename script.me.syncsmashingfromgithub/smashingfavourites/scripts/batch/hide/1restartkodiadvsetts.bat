@ECHO OFF

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
Timeout /T 2 /Nobreak
move E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\Thumbnails E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\OlderThumbnails
move E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\OldThumbnails E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\Thumbnails
move E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\savevideodbfile E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\olddb
move E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\savetexturesdbfile E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\olddb
move E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\newdb E:\XBMC Stuff\kryptonmess\portable_data\userdata\test\Database\
Timeout /T 2 /Nobreak
START "" "E:\XBMC Stuff\kryptonmess\kodi.exe" -p