# -*- coding: utf-8 -*-
# backtohome.py
# go back to home page 1 step at a time
import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# Check where we are
# if necessary go back 1 level
# repeat until at home screen
printstar()
c = 0
while c < 10:
    if not xbmc.getCondVisibility("Window.Is(home)"):
        try:
            xbmc.executebuiltin( "XBMC.Action(Back)" )
            c = c + 1
            print ('c is %d' % c)
        except:
            xbmc.sleep(100)
    else:
        c = 10
if not xbmc.getCondVisibility("Window.Is(home)"):
    xbmc.executebuiltin( "ActivateWindow(Home)" )
    print 'Going home'

# Drink beer        
