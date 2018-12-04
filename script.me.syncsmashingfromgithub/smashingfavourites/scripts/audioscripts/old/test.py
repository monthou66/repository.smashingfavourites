import xbmc
import os
import sys
from subprocess import call

profile = sys.argv[1]
btdevice = sys.argv[2]
profint = int(profile)

# read 'current profile' from script.audio.profiles  
currprof = open('/storage/.kodi/userdata/addon_data/script.audio.profiles/profile', 'r')

# change current profile integer to string
currint = currprof.read()
current = str(currint)

# for me 1 = HDMI TV // 2 = Bluetooth // 3 = HDMI amp //4 = analogue
#print "profile requested is " + profile
#print "btdevice is " + btdevice
#print "current profile is " + current

# switch sound profiles to wanted one (if necessary)
if profile != current:
    xbmc.executebuiltin("RunScript(script.audio.profiles,%s)" % (profint)) 


# if bluetooth selected connect chosen bluetooth receiver
# 
if profint == 2:
#   call('echo -e "connect ##YOUR-BT-MAC##\nexit" | bluetoothctl', shell=True)
    call('echo -e "connect 00:1F:81:08:25:AB\nexit" | bluetoothctl', shell=True)
# white usb call('echo -e "connect 00:1F:81:08:25:AB\nexit" | bluetoothctl', shell=True)	
 #   call('echo -e "connect %s\nexit" | bluetoothctl', shell=True % btdevice)


