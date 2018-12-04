# -*- coding: utf-8 -*-
# get masterprofile
# smashtoflashall.py
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
shellfile = os.path.join(folder, "flashtosmashall.sh")	
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
#    xbmc.executebuiltin('Notification(ohyeah, jose)')
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print "flashtosmashall.py has just been started"
printstar()