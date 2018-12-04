import xbmc
import os
from subprocess import call

# connect bluetooth receiver by mac address
#    call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
call('echo -e "connect E8:28:AB:12:86:21\nexit" | bluetoothctl', shell=True)
