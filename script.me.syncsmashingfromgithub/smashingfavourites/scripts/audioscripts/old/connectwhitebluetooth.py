import xbmc
import os
from subprocess import call

# switch sound profiles to bluetooth
xbmc.executebuiltin("RunScript(script.audio.profiles,2)")

# connect bluetooth receiver
#    call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
call('echo -e "connect 00:1F:81:08:25:AB\nexit" | bluetoothctl', shell=True)