#!/bin/sh
case "$1" in
pre)
;;
post)
printstar="***************************************************************************************"
log_file="/storage/.kodi/temp/kodishell.log"
echo "shelltest1 has started" >> $log_file

;;
esac