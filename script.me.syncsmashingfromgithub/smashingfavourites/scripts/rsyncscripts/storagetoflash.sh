#!/bin/sh
# Set your own variables
# TARGET_MOUNTPOINT=/var/media/mybackup
# TARGET_DIR=$TARGET_MOUNTPOINT/Media
TARGET=/flash/stuff/backups/storage
SOURCE=/storage/* 
RSYNC_OPTIONS="--recursive --verbose --itemize-changes --times --delete --human-readable"



# Append --dry-run to rsync call if test run only
if [ "$1" = "-t" -o "$1" = "--test" -o "$1" = "--dry-run" -o "$1" = "-n" ]; then
    RSYNC_OPTIONS="$RSYNC_OPTIONS --dry-run"
    echo "This is a DRY RUN only!"
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE_DIR" -a -d "$TARGET_DIR" ]; then
    # Mount flash rw
    mount -o remount,rw /flash
	echo "Backing up $SOURCE/* $TARGET"
#	rsync $RSYNC_OPTIONS $SOURCE_DIR/* $TARGET_DIR
	rsync $RSYNC_OPTIONS $SOURCE $TARGET
    # Mount flash ro
    mount -o remount,ro /flash
else
	echo "Error: Target or source dir not found!"
	exit 1 
fi