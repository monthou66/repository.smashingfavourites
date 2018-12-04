#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
def printscript():
    print "Running checkwindowandfocus.py"	
	
# check open window and focus - need to know whether favourites sideblade is open / whether to move focus if in a list
name = xbmc.getInfoLabel('currentwindow')
win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
focus = win.getFocusId()
control = xbmc.getInfoLabel('System.CurrentControl')
#try:
dialog = xbmcgui.getCurrentWindowDialogId()
# check if favourites window is visible - no returns 0, yes returns 1
vis = xbmc.getCondVisibility('Window.IsVisible(10134)')
if vis == 1:
    fav = ""
else:
    fav = "not"
if len(sys.argv) > 1:
    sarg = sys.argv[1]
    print ('sys.argv[1] is %s'% sarg)
    if sarg == 'back' or 'Back':
        xbmc.executebuiltin( "XBMC.Action(Back)" )
        xbmc.executebuiltin( "XBMC.Action(Left)" )
        xbmc.executebuiltin( "XBMC.Action(Right)" )
        print 'going back'
        xbmc.sleep(1000)
name = xbmc.getInfoLabel('currentwindow')
win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
window = xbmcgui.getCurrentWindowId()
focus = win.getFocusId()
control = xbmc.getInfoLabel('System.CurrentControl')	
printstar()
printscript()
print ("Current window is %s" % name)
print ("Current control is %s" % control)
print ("Current window id is %s" % win)
print ("window is %s" % window)
print ("Focus is %s" % focus)
print ("Favourites window is %s visible" % fav)
print ('CurrentWindowDialogID is %s'% dialog)
printstar()
xbmc.executebuiltin('Notification(Check log, for results)')
exit()