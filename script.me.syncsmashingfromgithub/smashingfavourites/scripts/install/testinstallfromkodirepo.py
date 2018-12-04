# -*- coding: utf-8 -*-

import xbmc
import xbmcgui

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "testinstallfromkodirepo.py has just been started"
printstar()
xbmc.executebuiltin('Notification(testinstallfromkodirepo.py, started)')
# addon = 'weather.yahoo'
addon = 'plugin.program.simple.favourites'
xbmc.executebuiltin('InstallAddon(%s)'% addon)
xbmc.sleep(1000)
xbmc.executebuiltin('SendClick(11)')
d = 0
while d < 100:
    xbmc.sleep(2000)
    if xbmcgui.getCurrentWindowDialogId() == 10101:
        xbmc.sleep(1000)
    elif xbmc.getCondVisibility('System.HasAddon(%s)' % addon):
        xbmc.executebuiltin('Notification(bloody, great)')
        d = 101
    else:
        d = d + 1
        e = d/5
        if e == int(e):
            xbmc.executebuiltin('Notification(hang on, a tick)')
if  not xbmc.getCondVisibility('System.HasAddon(%s)' % addon):
    printstar()
    print('cannot install %s from repo'% addon)
    printstar()
    xbmc.executebuiltin('Notification(bloody, hell)')







