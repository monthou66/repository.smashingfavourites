# -*- coding: utf-8 -*-

import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "install3.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1.py, started)')

CONFLUENCE = os.path.join(xbmc.translatePath('special://home/'), "addons", "skin.confluence")

xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "skin.confluence","enabled":false}}')
xbmc.sleep(300)
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "skin.confluence","enabled":true}}')
xbmc.sleep(300)

xbmc.executebuiltin('UpdateLocalAddons')
xbmc.executebuiltin('Notification(Starting, now)')
xbmc.executebuiltin('InstallAddon(skin.confluence)')
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
xbmc.sleep(300)

c = 0
while not os.path.isdir(CONFLUENCE):
    xbmc.sleep(1000)
    c = c + 1
    if c > 120:
        printstar()
        print 'wibble'
        printstar()
        exit()		
xbmc.sleep(1000)
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.confluence"}}')
xbmc.executebuiltin('SendClick(11)')		
xbmc.sleep(1000)
		
xbmc.executebuiltin('Notification(Done, Who\'d\'ve thunk it?)')