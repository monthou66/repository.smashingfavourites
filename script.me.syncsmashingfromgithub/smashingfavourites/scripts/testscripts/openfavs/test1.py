# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
#xbmc.executebuiltin('Notification(test1.py, started)')

c = 0
while c < 100:
    vis = xbmc.getCondVisibility('Window.IsVisible(10000)')
    if vis == 1:
        xbmc.executebuiltin("ActivateWindow(Favourites)")
        c = 100
        exit()
    else:
        xbmc.sleep(300)
        c = c + 1
exit()