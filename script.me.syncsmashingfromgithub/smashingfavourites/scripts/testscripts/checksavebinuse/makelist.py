# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil
# To show up in log:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def printworking():
    print "smashingxonf is doing stuff."
	
def printproblem():
    print "There is a problem with smashingxonfluence."
	
def printabandon():
    print "Script ended by user."
	
def printnorestore():
    print "No restore performed."
	
def printnobackup():
    print "No backup performed."
	
def printbackup():
    print "Xonfluence has been backed up."
	
def backupdone():
    xbmc.executebuiltin('Notification(Xonfluence has been, backed up)')
	
# Try generate list
FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/")
dialog = xbmcgui.Dialog()

restorechoose = dialog.browse(3, 'Choose backup to restore', 'files', '', False, False, False, 'special://masterprofile/smashing/smashingfavourites/backups/skins/xonfluence')
	
# restorechoose = xbmcgui.Dialog().browse(3, "Choose backup to restore", 'files, '', False, False, False, 'special://masterprofile/smashing/smashingfavourites/backups/skins/xonfluence')

# restorechoose = xbmcgui.Dialog(FOLDER).browse(0, "Choose backup to restore", 'files')

# restorechoose = xbmcgui.Dialog().browse(type, heading, shares[, mask, useThumbs, treatAsFolder, defaultt, enableMultiple])

print restorechoose






