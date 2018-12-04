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

# connect bluetooth receiver by mac address
#    call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
call('echo -e "connect 00:11:67:85:63:60\nexit" | bluetoothctl', shell=True)

  import xbmc 
  import os 
  From subprocess import call 
  Call ( 'echo -e "connect' ## BT-MAC address #" | bluetoothctl ', shell = true)
