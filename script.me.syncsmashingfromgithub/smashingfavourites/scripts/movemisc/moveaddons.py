# -*- coding: utf-8 -*-

import xbmc
import os
import shutil
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test3.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test3.py, started)')

ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/'), "addons")
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGADDONSFOLDER = os.path.join(SMASHINGFAVOURITES, "miscfiles", "addons")

ADDONS = []
ADDONS = os.listdir(ADDONSFOLDER)

SMASHINGADDONS = []
SMASHINGADDONS = os.listdir(SMASHINGADDONSFOLDER)

# remove duplicates:
# new_ra = [v for v in ra if v not in quad]
# ADDONSTOMOVE = []

ADDONSTOMOVE = [v for v in SMASHINGADDONS if v not in ADDONS]

for x in ADDONSTOMOVE:
    SMASH = os.path.join(SMASHINGFAVOURITES, "miscfiles", "addons", x)
#    print('SMASH is %s' % SMASH)
    REAL = os.path.join(ADDONSFOLDER, x)
#    shutil.copy(SMASH,REAL)
    shutil.copytree(SMASH,REAL)
#    shutil.copytree(SMASH, ADDONSFOLDER)
#    print ('REAL is %s' % REAL)
	
print ('ADDONS in addons folder are %s' % ADDONS)

print ('SMASHINGADDONS in miscfiles are %s' % SMASHINGADDONS)

print ('ADDONSTOMOVE in miscfiles are %s' % ADDONSTOMOVE)

NUM = len(SMASHINGADDONS)
print ('There are %d addons to copy' % NUM)


