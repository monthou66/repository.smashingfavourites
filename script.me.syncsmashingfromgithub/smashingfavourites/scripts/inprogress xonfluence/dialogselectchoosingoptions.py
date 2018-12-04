# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os

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
	
# Make list of options

XONFOPTION = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/xonfoption.txt")

if os.path.exists(XONFOPTION):
    f = open(XONFOPTION)
    OPTION = (f.read())		
    h = len(OPTION)
    f.close()
# remove backup pointers if no backup exists
    if h == 0:
        OPTION = 'None'	
    elif h > 0:
        CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/%s.txt" % OPTION)
        if not os.path.exists(CHECK):
            os.remove(XONFOPTION)
            OPTION = 'None'
else:
    OPTION = 'None'
	
OPTIONSLIST = ['Backup', 'Restore']
BACKUPSLIST = ['Backup latest', 'Backup existing', 'New backup']
FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/backups/")


BACKUPORRESTORE = xbmcgui.Dialog().select("Options", OPTIONSLIST)
if BACKUPORRESTORE == 0:
    CHOOSE = xbmcgui.Dialog().select("Options", BACKUPSLIST)    
    if CHOOSE == 0:
        CHOICE = ('Backup latest (%s)' % OPTION)
    elif CHOOSE == 1:
        CHOICE = 'Backup an existing folder'
    elif CHOICE == 2:
        CHOICE = 'Make a new backup'
else:
    CHOICE = 'Not applicable'
print ('BACKUPORRESTORE value is %d' % BACKUPORRESTORE)	
print CHOICE