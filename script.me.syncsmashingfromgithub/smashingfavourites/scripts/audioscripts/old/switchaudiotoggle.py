import xbmc
import os
from subprocess import call
# Original audio script from libreelec thread.  Not used now.
# switch sound profiles
xbmc.executebuiltin("RunScript(script.audio.profiles,0)")

# read 'current profile' from script.audio.profiles  
current = open('/storage/.kodi/userdata/addon_data/script.audio.profiles/profile', 'r')

# for me 1 = surround // 2 = blueTooth
# logical would say 'if 2' then connect the BT headset
# but audioProfiles takes some time to make the change & update the 'current' file
# so instead 'if 1 connect' (we know it will become 2 soon)
if current.read() == '1':
#     call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
      call('echo -e "connect 00:11:67:85:63:60\nexit" | bluetoothctl', shell=True)
current.close()