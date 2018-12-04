# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "testchannelswitch.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1.py, started)')

xbmc.executebuiltin( "XBMC.Action(Right)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Select)" )
exit()
