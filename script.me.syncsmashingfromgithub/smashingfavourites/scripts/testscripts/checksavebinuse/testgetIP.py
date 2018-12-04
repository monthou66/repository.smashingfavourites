# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

ip = xbmc.getIPAddress()
	
	
	
	
	
printstar()
print "test4.py has just been started"
print ('IP is %s' % ip)
printstar()
xbmc.executebuiltin('Notification(test4.py, started)')