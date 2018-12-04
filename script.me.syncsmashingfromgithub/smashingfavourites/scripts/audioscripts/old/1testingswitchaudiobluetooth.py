import xbmc
import os
import sys
from subprocess import call

profile = sys.argv[1]
btdevice = sys.argv[2]

# read 'current profile' from script.audio.profiles  
current = open('/storage/.kodi/userdata/addon_data/script.audio.profiles/profile', 'r')

# for me 1 = HDMI TV // 2 = Bluetooth // 3 = HDMI amp //4 = analogue
print "profile is " + profile
print "btdevice is" + btdevice

# switch sound profiles to bluetooth
#tempxbmc.executebuiltin("RunScript(script.audio.profiles,2)")

# connect bluetooth receiver
#    call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
#tempcall('echo -e "connect 00:11:67:85:63:60\nexit" | bluetoothctl', shell=True)
