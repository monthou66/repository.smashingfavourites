# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "install6.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(install6.py, started)')

# Define places - some might not be needed yet
USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISCFILES = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONDATA = os.path.join(MISCFILES, "addon_data")
# markers:
FAVOURITESFILE = os.path.join(USERDATA, "favourites.xml")
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
LOGFOLDER = xbmc.translatePath('special://logpath')
OLDLOGFILE = os.path.join(LOGFOLDER, "kodi.old.log")
# Check if this is a 'new' install.  Look for markers, prompt to refresh if necessary?
if os.path.exists(FAVOURITESFILE):
elif os.path.exists(ADVANCEDSETTINGS):
elif os.path.exists(OLDLOGFILE):
    NEWQUERY = xbmcgui.Dialog().yesno("This doesn't look like a new install","Do you want to carry on?")

	
	
# check nothing in SMASHINGADDONDATA is already in ADDONDATA.
# if there are duplicates end with message

ADDONDATATOPUSH = []
ADDONDATATARGET = []

ADDONDATATOPUSH = os.listdir(SMASHINGADDONDATA)
ADDONDATATARGET = os.listdir(ADDONDATA)
ALREADYTHERE = []
DUPLICATES = []
for i in ADDONDATATOPUSH:			 
    if i in ADDONDATATARGET:
        REPLACE = xbmcgui.Dialog().yesno("An addon-data folder already exists for %s" % i,"Do you want to replace it with the data from smashing favourites?")
        if REPLACE:
            TARGET = os.path.join(ADDONDATA, i)
#            print ('TARGET is %s' % TARGET)
#            exit()
            shutil.rmtree(TARGET)
            ALREADYTHERE.append(i)
        else:
	        DUPLICATES.append(i)
DUPS = len(DUPLICATES)
ALREADY = len(ALREADYTHERE)
if DUPS > 0 or ALREADY > 0:
    printstar()
    if DUPS > 0:
        print ('You have data already in the addon_data folder that will not be replaced: %s' % DUPLICATES)
    if ALREADY > 0:
        print ('You have data already in the addon_data folder that will be replaced: %s' % ALREADYTHERE)
    printstar()
#    exit()
	
for i in ADDONDATATOPUSH:
        if not i in DUPLICATES:
            SRC = os.path.join(SMASHINGADDONDATA, i)
            DEST = os.path.join(ADDONDATA, i)
            print ('SRC = %s' % SRC)
            print ('DEST = %s' % DEST)
            shutil.copytree(SRC, DEST)
printstar()
print 'By eck we\'re all done lad.'
printstar()
exit()
