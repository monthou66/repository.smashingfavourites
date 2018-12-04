# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')

xbmc.executebuiltin("ActivateWindow(10021)")
xbmc.executebuiltin( "XBMC.Action(Right)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Down)" )
xbmc.executebuiltin( "XBMC.Action(Select)" )
xbmc.executebuiltin('SendClick(11)')
# xbmc.sleep(300)
# xbmc.executebuiltin( "XBMC.Action(Back)" )
xbmc.executebuiltin("ActivateWindow(Home)")
