# -*- coding: utf-8 -*-
import os
import os.path
import xbmc
import xbmcaddon
import shutil
import sys
import xbmcgui

NAME = sys.argv[1]
win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
focus = win.getFocusId()

TEMPFAVOURITESFILE = os.path.join(xbmc.translatePath('special://userdata/'), "favourites", NAME, "favourites.xml")
REALFAVOURITESFILE = os.path.join(xbmc.translatePath('special://userdata'), "favourites.xml")
REALFAVOURITESSAVE = os.path.join(xbmc.translatePath('special://userdata'), "favouritessave.xml")
REALFAVOURITESBACKUP = os.path.join(xbmc.translatePath('special://userdata'), "favouritesbackup.xml")

# check if REALFAVOURITESSAVE file exists - if it does it means someone's button-happy
# so move REALFAVOURITESSAVE back to REALFAVOURITESFILE and close the script.
if os.path.isfile(REALFAVOURITESSAVE):
    os.remove(REALFAVOURITESFILE)
    os.rename(REALFAVOURITESSAVE, REALFAVOURITESFILE)
    exit    

# check if favourites window is visible - no returns 0, yes returns 1
vis = xbmc.getCondVisibility('Window.IsVisible(10134)')
#if favourites are visible move left to close them
if vis == 1:
	xbmc.executebuiltin( "XBMC.Action(Left)" )
	xbmc.sleep(300)

#	Check if using smashingletters whether focus is not on sidebar (2) or (right) scrollbar (60) - and move focus to main list if required.
if NAME == 'smashingletters':
	if focus == 2:
		xbmc.executebuiltin( "XBMC.Action(Right)" )
	if focus == 60:
		xbmc.executebuiltin( "XBMC.Action(Left)" )		
	
#  Rename favourites.xml to favouritessave.xml, copy temp favourites to userdata, load favourites, restore real favourites.

if os.path.isfile(REALFAVOURITESFILE):
    os.rename(REALFAVOURITESFILE, REALFAVOURITESSAVE)
    shutil.copy(TEMPFAVOURITESFILE, REALFAVOURITESFILE)
    xbmc.executebuiltin("ActivateWindow(Favourites)")
    xbmc.sleep(1000)
    os.remove(REALFAVOURITESFILE)
    os.rename(REALFAVOURITESSAVE, REALFAVOURITESFILE)
    exit
else:
    shutil.copy(TEMPFAVOURITESFILE, REALFAVOURITESFILE)
    xbmc.executebuiltin("ActivateWindow(Favourites)")
    xbmc.executebuiltin('Notification(Check, favourites)')
    xbmc.sleep(1000)
    os.remove(REALFAVOURITESFILE)
    shutil.copy(REALFAVOURITESBACKUP, REALFAVOURITESFILE)
    exit