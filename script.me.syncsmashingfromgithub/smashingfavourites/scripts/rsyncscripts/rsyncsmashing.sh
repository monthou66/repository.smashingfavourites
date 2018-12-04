#!/bin/sh
# rsynctoflash.sh
# Set variables from smashingfavourites/tempfiles/TARGET.txt and smashingfavourites/tempfiles/SOURCE.txt

TARGET=/flash/stuff/backuptest
SOURCE=/storage 
RSYNC_OPTIONS="--recursive --ignore-existing --verbose --itemize-changes --human-readable"



# Append --dry-run to rsync call if test run only
if [ "$1" = "-t" -o "$1" = "--test" -o "$1" = "--dry-run" -o "$1" = "-n" ]; then
    RSYNC_OPTIONS="$RSYNC_OPTIONS --dry-run"
    echo "This is a DRY RUN only!"
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE" -a -d "$TARGET" ]; then
    # Mount flash rw
    mount -o remount,rw /flash
	echo "Backing up $SOURCE/* $TARGET"
	rsync $RSYNC_OPTIONS $SOURCE $TARGET
    # Mount flash ro
    mount -o remount,ro /flash
else
	echo "Error: Target or source dir not found!"
	exit 1 
fi