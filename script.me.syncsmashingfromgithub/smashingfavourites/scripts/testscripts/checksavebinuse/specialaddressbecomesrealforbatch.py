# -*- coding: utf-8 -*-

import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test3.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test3.py, started)')

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
FOLDERSPATH = os.path.join(SMASHINGFAVOURITES, "advancedsettings")

printstar()
print ('USERDATA = %s' % USERDATA)
print ('SMASHINGFAVOURITES = %s' % SMASHING)
print ('FOLDERSPATH = %s' % FOLDERSPATH)
printstar()	