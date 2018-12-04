#!/bin/sh
# smashtoflash.sh

TARGET=/storage/.kodi/userdata
SOURCE=/flash/stuff/backups
SOURCESMASHFAVS=/flash/stuff/backups/smashing/smashing/smashingfavourites/*
TARGETSMASHFAVS=/storage/.kodi/userdata/smashing/smashingfavourites
#SOURCESPECS=/flash/stuff/backups/smashing/smashingspecifics/*
#TARGETSPECS=/storage/.kodi/userdata/smashing/smashingspecifics
SOURCEFAV=/flash/stuff/backups/smashing/favourites.xml
TARGETFAV=/storage/.kodi/userdata/favourites.xml
# RSYNC_OPTIONS="--recursive --ignore-existing --verbose --itemize-changes --human-readable"
RSYNC_OPTIONS="--recursive --verbose --itemize-changes --human-readable"


# Append --dry-run to rsync call if test run only
if [ "$1" = "-t" -o "$1" = "--test" -o "$1" = "--dry-run" -o "$1" = "-n" ]; then
    RSYNC_OPTIONS="$RSYNC_OPTIONS --dry-run"
    echo "This is a DRY RUN only!"
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE" -a -d "$TARGET" ]; then
	echo "Backing up SMASHING"
	rsync $RSYNC_OPTIONS $SOURCESMASHFAVS $TARGETSMASHFAVS
#	rsync $RSYNC_OPTIONS $SOURCESPECS $TARGETSPECS
#	rsync $RSYNC_OPTIONS $SOURCEFAV $TARGETFAV
else
	echo "Error: Target or source dir not found!"
	exit 1 
fi