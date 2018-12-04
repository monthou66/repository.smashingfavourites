#!/bin/sh
case "$1" in
pre)
;;
post)
if mountpoint -q "/dev/sdc1"; then
    reboot
else
    poweroff

;;
esac