# -*- coding: utf-8 -*-
# clonepvr.iptvsimple.py
# This clones pvr.iptvsimple automativally when it updates.

import xbmc
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "clonepvr.iptvsimple.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(test1cloneaddon.py, started)')

# define file locations
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
PVRIPTVSIMPLE = os.path.join(ADDONS, "pvr.iptvsimple")
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/pvr.iptvsimple'))
CLONEADDON = os.path.join(ADDONS, "pvr.iptvsimplefab")
XML = os.path.join(CLONEADDON, "addon.xml")
XMLIN = os.path.join(CLONEADDON, "addon.xml.in")
DLLOLD = os.path.join(CLONEADDON, "pvr.iptvsimple.dll")
DLLNEW = os.path.join(CLONEADDON, "pvr.iptvsimplefab.dll")
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISC, "addons")
OLDADDONS = os.path.join(SMASHINGADDONS, "oldaddons")
OLDCLONE = os.path.join(OLDADDONS, "pvr.iptvsimplefab")
OLDCLONEDLL = os.path.join(OLDCLONE, "pvr.iptvsimplefab.dll")
MARKERSOURCE = os.path.join(OLDADDONS, "cloned.txt")

# print 'PVRIPTVSIMPLE is %s'% PVRIPTVSIMPLE
# print 'ALTERNATE is %s'% ALTERNATE
# print 'CLONEADDON is %s'% CLONEADDON
# print 'XML is %s'% XML
# print 'XMLIN is %s'% XMLIN
# print 'OLDCLONE is %s'% OLDCLONE
# print 'MARKERSOURCE is %s'% MARKERSOURCE

#  exit()

# if pvr.iptvsimple is there but MARKER doesn't exist we need to update CLONEADDON - otherwise exit
# if not there check for default install (ie windows!)
if not os.path.exists(PVRIPTVSIMPLE):
    print 'PVRIPTVSIMPLE does not exist.'
    if not os.path.exists(ALTERNATE):
        print 'ALTERNATE does not exist either.'
        printstar()
        print 'pvr.iptvsimple is not installed, so cannot be cloned.'
        printstar()	
        exit()
    else:
        PVRIPTVSIMPLE = ALTERNATE
MARKER = os.path.join(PVRIPTVSIMPLE, "cloned.txt")
if os.path.isfile(MARKER):
    if os.path.exists(CLONEADDON):
        xbmc.executebuiltin('Notification(pvr.iptvsimplefab does not need, to be updated)')
        printstar()
        print 'pvr.iptvsimple checked - all is well.'
        printstar()
        exit()
# Looks like we need to update:

# - disable the addon if it's enabled
#if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):
#    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "pvr.iptvsimplefab","enabled":false}}')
#    xbmc.sleep(1000)
#    xbmc.executebuiltin('Notification(pvr.iptvsimplefab, has been disabled)')

# - delete backup if it exists
# - check clone folder exists
# - if it does move clone folder into backup location
# - copy pvr.iptvsimple folder to clone folder
# - make new MARKER file and put in place
# - edit addon.xml and addon.xml.in
# - update local addons
#if os.path.exists(OLDCLONE):
#    if os.path.isfile(OLDCLONEDLL):
#        os.remove(OLDCLONEDLL)
if os.path.exists(OLDCLONE):
    shutil.rmtree(OLDCLONE)
if os.path.exists(CLONEADDON):
    shutil.move(CLONEADDON, OLDADDONS)
    xbmc.executebuiltin('Action(UpdateLocalAddons)')
    xbmc.sleep(300)
    
shutil.copytree(PVRIPTVSIMPLE, CLONEADDON)
shutil.copy(MARKERSOURCE, PVRIPTVSIMPLE)

# Replace variables in file
with open(XML, 'r+') as f:
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace('pvr.iptvsimple', 'pvr.iptvsimplefab'))
with open(XML, 'r+') as f:
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace('PVR IPTV Simple Client', 'PVR IPTV Simple Client fab'))
with open(XMLIN, 'r+') as f:
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace('pvr.iptvsimple', 'pvr.iptvsimplefab'))
with open(XMLIN, 'r+') as f:
    content = f.read()
    f.seek(0)
    f.truncate()
    f.write(content.replace('PVR IPTV Simple Client', 'PVR IPTV Simple Client fab'))
if os.path.isfile(DLLOLD):
#    os.rename(DLLOLD, DLLNEW)
    shutil.copy(DLLOLD, DLLNEW)
    os.remove(DLLOLD)
    
    

    
    
    
    
else:
   xbmc.executebuiltin('Notification(Problem renaming .dll file, see log for details)') 
   printstar()
   print 'Could not rename pvr.iptvsimple.dll to pvr.iptvsimplefab.dll'
   print 'Do it manually before enabling pvr.iptvsimplefab'
   printstar()
   exit()
xbmc.sleep(300)
xbmc.executebuiltin('Action(UpdateLocalAddons)')
xbmc.sleep(300)
# if not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "pvr.iptvsimplefab","enabled":true}}')
xbmc.executebuiltin('Notification(pvr.iptvsimplefab, updated)')
printstar()
print 'pvr.iptvsimplefab has been updated.'
printstar()
exit()

# Drink beer



