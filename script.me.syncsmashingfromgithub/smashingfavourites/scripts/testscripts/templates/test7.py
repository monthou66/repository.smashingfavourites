# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test7.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test2.py, started)')