# -*- coding: utf-8 -*-
import os
import os.path
import xbmc
import xbmcaddon
import shutil
import sys
import xbmcgui

FAVOURITESFILE = os.path.join(xbmc.translatePath('special://userdata'), "favourites.xml")
FAVOURITESBACKUP = os.path.join(xbmc.translatePath('special://userdata'), "favouritesbackup.xml")
FAVOURITESBACKUPOLD = os.path.join(xbmc.translatePath('special://userdata'), "favouritesbackupold.xml")

#	Copy favourites.xml to favouritesbackup.xml - make an 'extra' backup of the old backup for emergencies.	

if os.path.isfile(FAVOURITESFILE) and os.path.isfile(FAVOURITESBACKUP):
    os.rename(FAVOURITESBACKUP, FAVOURITESBACKUPOLD)
    shutil.copy(FAVOURITESFILE, FAVOURITESBACKUP)
    xbmc.executebuiltin('Notification(Favourites, saved)')	
    xbmc.executebuiltin( "XBMC.Action(Back)" )
    xbmc.sleep(300)	
    xbmc.executebuiltin("ActivateWindow(Favourites)")

else:
    xbmc.executebuiltin('Notification(Problem, - no backup made)')