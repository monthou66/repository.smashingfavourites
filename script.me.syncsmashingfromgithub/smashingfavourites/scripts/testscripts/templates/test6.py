# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test6.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')