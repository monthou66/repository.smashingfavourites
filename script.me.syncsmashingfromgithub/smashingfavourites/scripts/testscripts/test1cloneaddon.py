# -*- coding: utf-8 -*-
# make addon.py
# This clones pvr.iptvsimple automativally when it updates.

import xbmc
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1cloneaddon.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1cloneaddon.py, started)')

# define file locations
PVRIPTVSIMPLE = os.path.join(xbmc.translatePath('special://home/addons/pvr.iptvsimple'))
MARKER = os.path.join(PVRIPTVSIMPLE, "cloned.txt")
CLONEDADDON = os.path.join(xbmc.translatePath('special://home/addons/pvr.iptvsimplefab'))
XML = os.path.join(CLONEDADDON, "addon.xml")
XMLIN = os.path.join(CLONEDADDON, "addon.xml.in")
OLDCLONE = os.path.join(xbmc.translatePath('special://masterprofile/smashing/smashingfavourites/miscfiles/oldaddons/pvr.iptvsimplefab'))
MARKERSOURCE = os.path.join(xbmc.translatePath('special://masterprofile/smashing/smashingfavourites/miscfiles/oldaddons/'), "cloned.txt")

# if pvr.iptvsimple is there but MARKER doesn't exist we need to update CLONEADDON - otherwise exit
if not os.path.exists(PVRIPTVSIMPLE):
    printstar()
    print 'pvr.iptvsimple is not installed, so can't be cloned.'
    printstar()	
    exit()
if os.path.isfile(MARKER):
    printstar()
    print 'pvr.iptvsimple checked - all is well.'
    printstar()
    exit()
# Looks like we need to update:
# - delete backup if it exists
# - check clone folder exists
# - if it does move clone folder into backup location
# - copy pvr.iptvsimple folder to clone folder
# - make new MARKER file and put in place
# - edit addon.xml and addon.xml.in
# - update local addons
if os.path.exists(OLDCLONE):
    shutil.rmtree(OLDCLONE)
if os.path.exists(CLONEADDON):
    os.rename(CLONEADDON, OLDCLONE)
shutil.copytree(PVRIPTVSIMPLE, CLONEADDON)
shutil.copy(MARKERSOURCE, PVRIPTVSIMPLE)

# Replace variables in file
with open(XML, 'r+') as f:
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace('pvr.iptvsimple', 'pvr.iptvsimplefab'))
    f.write(content.replace('PVR IPTV Simple Client', 'PVR IPTV Simple Client fab'))
with open(XMLIN, 'r+') as f:
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace('pvr.iptvsimple', 'pvr.iptvsimplefab'))
    f.write(content.replace('PVR IPTV Simple Client', 'PVR IPTV Simple Client fab'))

xbmc.sleep(300)
xbmc.executebuiltin('Action(UpdateLocalAddons)')
xbmc.sleep(300)
xbmc.executebuiltin('Notification(pvr.iptvsimplefab, updated)')
printstar()
print 'pvr.iptvsimplefab has been updated.'
printstar()
exit()

# Drink beer



