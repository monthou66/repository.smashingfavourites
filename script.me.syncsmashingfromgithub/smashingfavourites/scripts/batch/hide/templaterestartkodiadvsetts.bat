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
move THUMBNAILSFOLDER oldthumbs
move newthumbs THUMBNAILSFOLDER
move savevideodbfile olddb
move savetexturesdbfile olddb
move newdb DATABASEFOLDER
Timeout /T 2 /Nobreak
START "" "E:\XBMC Stuff\kryptonmess\kodi.exe" -p