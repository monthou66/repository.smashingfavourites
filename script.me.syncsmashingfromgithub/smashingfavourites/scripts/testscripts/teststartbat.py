# -*- coding: utf-8 -*-
# teststartbat
import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "teststartbat.py has just been started"
printstar()
xbmc.executebuiltin('Notification(teststartbat.py, started)')