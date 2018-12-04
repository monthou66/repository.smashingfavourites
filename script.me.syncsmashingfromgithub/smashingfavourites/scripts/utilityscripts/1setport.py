# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

ip = xbmc.getIPAddress()
	
	
	
	
	
printstar()
print "test4.py has just been started"
print ('IP is %s' % ip)
xbmc.executebuiltin('Notification(IP address is, %s)'% ip)
printstar()


#port = 10002

port = 8080
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"services.webserverport","value":%d},"id":1}'% port)


