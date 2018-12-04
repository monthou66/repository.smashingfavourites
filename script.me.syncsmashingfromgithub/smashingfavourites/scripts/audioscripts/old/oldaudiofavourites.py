# -*- coding: utf-8 -*-
import os
import os.path
import xbmc
import xbmcaddon
import shutil

AUDIOFAVOURITESFILE = os.path.join(xbmc.translatePath('special://userdata/'), "favourites/audio/favourites.xml")
REALFAVOURITESFILE = os.path.join(xbmc.translatePath('special://userdata'), "favourites.xml")
REALFAVOURITESSAVE = os.path.join(xbmc.translatePath('special://userdata'), "favouritessave.xml")
REALFAVOURITESBACKUP = os.path.join(xbmc.translatePath('special://userdata'), "favouritesbackup.xml")

#  Rename favourites.xml to favouritessave.xml, copy audiofavourites to userdata, load favourites, restore real favourites.

if os.path.isfile(REALFAVOURITESFILE):
    os.rename(REALFAVOURITESFILE, REALFAVOURITESSAVE)
    shutil.copy(AUDIOFAVOURITESFILE, REALFAVOURITESFILE)
    xbmc.executebuiltin("ActivateWindow(Favourites)")
    xbmc.sleep(1000)
    os.remove(REALFAVOURITESFILE)
    os.rename(REALFAVOURITESSAVE, REALFAVOURITESFILE)
    exit
else:
    shutil.copy(AUDIOFAVOURITESFILE, REALFAVOURITESFILE)
    xbmc.executebuiltin("ActivateWindow(Favourites)")
    xbmc.executebuiltin('Notification(Check, favourites)')
    xbmc.sleep(1000)
    os.remove(REALFAVOURITESFILE)
    shutil.copy(REALFAVOURITESBACKUP, REALFAVOURITESFILE)
    exit