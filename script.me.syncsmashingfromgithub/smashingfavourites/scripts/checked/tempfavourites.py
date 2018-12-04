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

TEMPFAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashing", "smashingfavourites", NAME, "favourites.xml")
REALFAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile'), "favourites.xml")
REALFAVOURITESSAVE = os.path.join(xbmc.translatePath('special://masterprofile'), "favouritessave.xml")
REALFAVOURITESBACKUP = os.path.join(xbmc.translatePath('special://masterprofile'), "favouritesbackup.xml")

# check if REALFAVOURITESSAVE file exists - if it does it means someone's button-happy
# so move REALFAVOURITESSAVE back to REALFAVOURITESFILE and close the script.
if os.path.isfile(REALFAVOURITESSAVE):
    os.remove(REALFAVOURITESFILE)
    os.rename(REALFAVOURITESSAVE, REALFAVOURITESFILE)
    exit()    

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

#  Check if	the real favourites.xml is wanted, open it if required.
if NAME == 'realfavourites':
    xbmc.executebuiltin("ActivateWindow(Favourites)")
    exit()

#  Rename favourites.xml to favouritessave.xml, copy temp favourites to userdata, load favourites, restore real favourites.

if os.path.isfile(REALFAVOURITESFILE) and os.path.isfile(TEMPFAVOURITESFILE):
    os.rename(REALFAVOURITESFILE, REALFAVOURITESSAVE)
    shutil.copy(TEMPFAVOURITESFILE, REALFAVOURITESFILE)
    xbmc.executebuiltin("ActivateWindow(Favourites)")
else:
    xbmc.executebuiltin('Notification(Check, non-existentfile)')
    exit()
	
# move focus to top except in smashingletters
if NAME != "smashingletters":
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
	
# wait a bit	
xbmc.sleep(500)
# check realfavouritessave exists, and move it back into place
if os.path.isfile(REALFAVOURITESSAVE):
    os.remove(REALFAVOURITESFILE)
    os.rename(REALFAVOURITESSAVE, REALFAVOURITESFILE)
    exit()
else:
    os.remove(REALFAVOURITESFILE)
    shutil.copy(REALFAVOURITESBACKUP, REALFAVOURITESFILE)
    xbmc.executebuiltin('Notification(Check, favourites)')
    exit()	
