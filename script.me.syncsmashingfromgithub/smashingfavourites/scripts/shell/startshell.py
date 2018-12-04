# -*- coding: utf-8 -*-
# startshell.py

import xbmc
import os
import sys

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "shell")
filename = sys.argv[1]
shellfile = os.path.join(folder, "%s.sh"% filename)	
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
#    xbmc.executebuiltin('Notification(ohyeah, jose)')
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print ("startshell.py has just started %s.sh"% filename)
printstar()