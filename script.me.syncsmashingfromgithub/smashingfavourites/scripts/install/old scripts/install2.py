# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test6.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1.py, started)')

xbmc.executebuiltin('InstallAddon(skin.confluence)')
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
xbmc.sleep(300)

c = 0
if not xbmc.getCondVisibility('System.HasAddon(skin.confluence)'):
    xbmc.sleep(1000)
    c = c + 1
    if c > 120:
        printstar()
        print 'wibble'
        printstar()		
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.confluence"}}')
xbmc.executebuiltin('SendClick(11)')		
xbmc.sleep(1000)


xbmc.executebuiltin('InstallAddon(skin.amber)')
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
xbmc.sleep(300)

c = 0
if not xbmc.getCondVisibility('System.HasAddon(skin.amber)'):
    xbmc.sleep(1000)
    c = c + 1
    if c > 120:
        printstar()
        print 'wibble'
        printstar()		
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.amber"}}')
xbmc.executebuiltin('SendClick(11)')		
xbmc.sleep(1000)
		
xbmc.executebuiltin('InstallAddon(skin.titan)')
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
xbmc.sleep(300)

c = 0
if not xbmc.getCondVisibility('System.HasAddon(skin.titan)'):
    xbmc.sleep(1000)
    c = c + 1
    if c > 120:
        printstar()
        print 'wibble'
        printstar()	
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.titan"}}')
xbmc.executebuiltin('SendClick(11)')		
xbmc.sleep(5000)

xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.confluence"}}')
xbmc.executebuiltin('SendClick(11)')		
xbmc.sleep(1000)		
xbmc.executebuiltin('Notification(Done, Who\'d\'ve thunk it?)')