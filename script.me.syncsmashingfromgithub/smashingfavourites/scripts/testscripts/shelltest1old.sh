#!/bin/sh
case "$1" in
pre)
;;
post)
if /dev/sda1
then
         reboot
;;
esac