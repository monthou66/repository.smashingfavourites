#!/bin/sh
case "$1" in
pre)
;;
post)
systemctl stop kodi

mv THUMBNAILSFOLDER oldthumbs

mv newthumbs THUMBNAILSFOLDER

mv savevideodbfile olddb

mv savetexturesdbfile olddb

mv newdb DATABASEFOLDER

systemctl start kodi
;;
esac