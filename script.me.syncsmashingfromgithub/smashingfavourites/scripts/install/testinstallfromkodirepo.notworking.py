# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "testinstallfromkodirepo.py has just been started"
printstar()
xbmc.executebuiltin('Notification(testinstallfromkodirepo.py, started)')


xbmc.executebuiltin('InstallAddon(weather.yahoo)')
c = 0
while c < 150:
    xbmc.sleep(300)
    if xbmc.getCondVisibility('System.HasAddon(weather.yahoo)'):
        xbmc.executebuiltin('Notification(bloody, great)')
        xbmc.executebuiltin('SendClick(11)')
        xbmc.executebuiltin('Notification(weather.yahoo, installed)')
        c = 1000
    else:
        c = c + 1
        d = c/15
        if d == int(d):
            xbmc.executebuiltin('Notification(hang on, a tick)')
if c < 1000:
    xbmc.executebuiltin('Notification(bloody, hell)')
            
exit()






