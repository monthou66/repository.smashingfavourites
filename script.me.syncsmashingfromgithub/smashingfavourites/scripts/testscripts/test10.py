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
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "testscripts")
shellfile = os.path.join(folder, "shelltest1.sh")
        
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print "test9.py has just been started"
#print ('testy = %s' % testy)
printstar()
# xbmc.executebuiltin('Notification(test4.py, started)')
