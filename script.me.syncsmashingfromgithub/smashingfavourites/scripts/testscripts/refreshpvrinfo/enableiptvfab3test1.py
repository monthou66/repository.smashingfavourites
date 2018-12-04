# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')

if not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):
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
    printstar()
    print 'check 1'
    xbmc.sleep(1000)
    printstar()
    print 'check 2'
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":true}}')
    printstar()
    print 'check 3'
    xbmc.sleep(300)
xbmc.executebuiltin( "XBMC.Action(Select)" )
xbmc.executebuiltin('SendClick(11)')
xbmc.executebuiltin("ActivateWindow(Home)")
