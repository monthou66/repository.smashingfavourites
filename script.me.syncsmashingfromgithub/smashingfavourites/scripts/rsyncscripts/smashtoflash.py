# -*- coding: utf-8 -*-
# get masterprofile
# smashtoflash.py
import xbmc
import os
import sys

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "rsyncscripts")
#shellfile = os.path.join(folder, "rsyncssmashingtoflash.sh")
shellfile = os.path.join(folder, "rsyncstoragetousb.sh")
shellfile = os.path.join(folder, "smashtoflash.sh")	
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
#    xbmc.executebuiltin('Notification(ohyeah, jose)')
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print "rsyncsmashingtoflash.py has just been started"
printstar()