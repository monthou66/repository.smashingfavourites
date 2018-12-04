import xbmc
import os
from subprocess import call

# switch sound profiles to bluetooth
xbmc.executebuiltin("RunScript(script.audio.profiles,2)")

# connect bluetooth receiver
#    call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
call('echo -e "connect 00:11:67:85:63:60\nexit" | bluetoothctl', shell=True)

