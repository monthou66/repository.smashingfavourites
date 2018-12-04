#!/bin/sh
case "$1" in
pre)
;;
post)
printstar="***************************************************************************************"
log_file="/storage/.kodi/temp/kodishell.log"
echo "$printstar" >> $log_file
echo "shelltest1 has started" >> $log_file

sleep 1

#kodi-send --action="up"		works with sleep!!!!!!
#kodi-send -a "Notification(testing,testmessage)"	# works with sleep!!!!
#kodi-send --action="XBMC.Notification(testing,testmessage)"	# works with sleep!!!!

#kodi-send --action="Notification(testing,testmessage)"	# works with sleep!!!!


#kodi-send --action 'Notification(testing,testmessage)'	# works with sleep!!!!


;;
esac