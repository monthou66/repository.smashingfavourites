# -*- coding: utf-8 -*-

import xbmc
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "install5.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1.py, started)')

USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISCFILES = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONDATA = os.path.join(MISCFILES, "addon_data")

# check nothing in SMASHINGADDONDATA is already in ADDONDATA.
# if there are duplicates end with message

ADDONDATATOPUSH = []
ADDONDATATARGET = []

ADDONDATATOPUSH = os.listdir(SMASHINGADDONDATA)
ADDONDATATARGET = os.listdir(ADDONDATA)

DUPLICATES = []
for i in ADDONDATATOPUSH:			 
    if i in ADDONDATATARGET:
        DUPLICATES.append(i)
DUPS = len(DUPLICATES)
if DUPS > 0:
    printstar()
    print ('That ain\'t gonna fly.  You have duplicates in addon_data: %s' % DUPLICATES)
    printstar()
    exit()
	
for i in ADDONDATATOPUSH:
    SRC = os.path.join(SMASHINGADDONDATA, i)
    DEST = os.path.join(ADDONDATA, i)
    print ('SRC = %s' % SRC)
    print ('DEST = %s' % DEST)
    shutil.copytree(SRC, DEST)
printstar()
print 'By eck we\'re all done lad.'
printstar()
exit()
