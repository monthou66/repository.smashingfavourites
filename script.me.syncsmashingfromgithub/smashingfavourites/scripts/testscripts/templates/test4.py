# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test4.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test4.py, started)')