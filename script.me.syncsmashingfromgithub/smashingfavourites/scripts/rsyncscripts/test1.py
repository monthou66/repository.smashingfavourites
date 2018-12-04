# -*- coding: utf-8 -*-
# get masterprofile
import xbmc
import os
import system

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "rsyncscripts")
shellfile = os.path.join(folder, "rsyncssmashingtoflash.sh")
	
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print "rsyncsmashingtoflash.py has just been started"
printstar()