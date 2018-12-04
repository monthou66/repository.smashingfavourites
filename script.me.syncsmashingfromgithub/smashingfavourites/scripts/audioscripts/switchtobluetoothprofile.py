import xbmc
import os
from subprocess import call

# read 'current profile' from script.audio.profiles  
currprof = open('/storage/.kodi/userdata/addon_data/script.audio.profiles/profile', 'r')
current = currprof.read()

# for me 1 = HDMI TV // 2 = Bluetooth // 3 = HDMI amp //4 = analogue
# switch sound profiles to bluetooth (if necessary)

if current != 2:
    xbmc.executebuiltin("RunScript(script.audio.profiles,2)")

