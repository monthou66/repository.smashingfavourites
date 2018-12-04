# -*- coding: utf-8 -*-
# get masterprofile
import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "testshell")
shellfile = os.path.join(folder, "shelltest10.sh")
        
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
#    xbmc.executebuiltin('Notification(ohyeah, jose)')
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print "testshell10.py has just been started"
#print ('testy = %s' % testy)
printstar()
# xbmc.executebuiltin('Notification(testshell10.py, started)')
