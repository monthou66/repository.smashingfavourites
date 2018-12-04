# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test5.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')