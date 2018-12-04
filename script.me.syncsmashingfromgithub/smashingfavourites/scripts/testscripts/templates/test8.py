# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test8.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test3.py, started)')
	