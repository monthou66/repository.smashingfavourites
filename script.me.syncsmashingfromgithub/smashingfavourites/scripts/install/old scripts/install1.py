# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test6.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1.py, started)')

xbmc.executebuiltin('InstallAddon(skin.amber)')
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
xbmc.executebuiltin('InstallAddon(skin.titan)')
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
xbmc.executebuiltin('Notification(Done, Who\'d\'ve thunk it?)')