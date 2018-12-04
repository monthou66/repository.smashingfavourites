#!/bin/sh
# Set your own variables
TARGET_MOUNTPOINT=/var/media/mybackup
TARGET_DIR=$TARGET_MOUNTPOINT/Media
SOURCE_DIR=/storage 
RSYNC_OPTIONS="--recursive --ignore-existing --verbose --itemize-changes --human-readable"

# Append --dry-run to rsync call if test run only
if [ "$1" = "-t" -o "$1" = "--test" -o "$1" = "--dry-run" -o "$1" = "-n" ]; then
    RSYNC_OPTIONS="$RSYNC_OPTIONS --dry-run"
    echo "This is a DRY RUN only!"
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE_DIR/videos" -a -d "$TARGET_DIR/videos" ]; then
	echo "Backing up $SOURCE_DIR/videos/* $TARGET_DIR/videos"
	rsync $RSYNC_OPTIONS $SOURCE_DIR/videos/* $TARGET_DIR/videos
else
	echo "Error: Target or source dir not found!"
	exit 1 
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE_DIR/movies" -a -d "$TARGET_DIR/movies" ]; then
	echo "Backing up $SOURCE_DIR/movies/* $TARGET_DIR/movies"
	rsync $RSYNC_OPTIONS $SOURCE_DIR/movies/* $TARGET_DIR/movies
else
	echo "Error: Target or source dir not found!"
	exit 1
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE_DIR/tvshows" -a -d "$TARGET_DIR/tvshows" ]; then
	echo "Backing up $SOURCE_DIR/tvshows/* $TARGET_DIR/tvshows"
	rsync $RSYNC_OPTIONS $SOURCE_DIR/tvshows/* $TARGET_DIR/tvshows
else
	echo "Error: Target or source dir not found!"
	exit 1
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE_DIR/music" -a -d "$TARGET_DIR/music" ]; then
	echo "Backing up $SOURCE_DIR/music/* $TARGET_DIR/music"
	rsync $RSYNC_OPTIONS $SOURCE_DIR/music/* $TARGET_DIR/music
else
	echo "Error: Target or source dir not found!"
	exit 1
fi
# Check first if source and target dirs exist
if [ -d "$SOURCE_DIR/pictures" -a -d "$TARGET_DIR/pictures" ]; then
	echo "Backing up $SOURCE_DIR/pictures/* $TARGET_DIR/pictures"
	rsync $RSYNC_OPTIONS $SOURCE_DIR/pictures/* $TARGET_DIR/pictures
else
	echo "Error: Target or source dir not found!"
	exit 1
fi