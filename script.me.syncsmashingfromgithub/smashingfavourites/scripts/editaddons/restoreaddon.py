# -*- coding: utf-8 -*-
# restoreaddon.py
# This restores an addon from a backup in smashingtemp.

import xbmc
import xbmcgui
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "restoreaddon.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(editxonf.py, started)')

# define file locations
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/'))
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
BACKUPS = os.path.join(SMASHINGTEMP, "backups")

# check for backups in the backup folder
size = 0
if os.path.exists(BACKUPS):
    check = []
    contents = []
    check = os.listdir(BACKUPS)
    for k in check:
#        next = contents[k]
#        path = os.path.join(BACKUPS, next)
        path = os.path.join(BACKUPS, k)
#        print ('checking %s'% next)
        print ('checking %s'% k)
        if os.path.isdir(path):
#            contents.append(next)
            contents.append(k)
    size = len(contents)
if size == 0:
    printstar()
    print 'restoreaddon.py - no backups to restore'
    printstar()
    xbmc.executebuiltin('Notification(No backups, are available)')
    exit()
# choose option to restore:
CHOOSE = xbmcgui.Dialog().select("Select addon to restore:", contents)
CHOICE = contents[CHOOSE]
if not CHOOSE == -1:
    CHOSEN = contents[CHOOSE]
else:
    print'Script cancelled by user'
    xbmc.executebuiltin('Notification(Action, cancelled)')
    exit()

# Check for folder
SOURCE = os.path.join(BACKUPS, CHOSEN)
testpath = os.path.join(ADDONS, CHOSEN)
if not os.path.exists(testpath):
    altpath = os.path.join(ADDONS, CHOSEN)
    if os.path.exists(altpath):
        printstar()
        print 'Problem with restoreaddon.py'
        print ('Addon to restore is in the default addons folder: %s'% altpath)
        print 'Sort this out manually'
        printstar()
        xbmc.executebuiltin('Notification(Problem with restoreaddon.py, Check log for details)')
        exit()
else:
    # Check if addon is installed - disable if it is (and not the active skin!)
    if xbmc.getCondVisibility('System.HasAddon(%s)'% CHOSEN):
        # check if addon is current skin
        skindir = xbmc.getSkinDir()
        print ('skindir = %s'% skindir)
        if skindir == CHOSEN:
            print 'restoreaddon.py - change skin before restoring the current skin'
            xbmc.executebuiltin('Notification(Switch to a different skin, and try again)')
            exit()
        else:
            # disable the addon
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":false}}' % CHOSEN)
            xbmc.sleep(300)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
                printstar()
                print 'Problem with restoreaddon.py'
                print ('Failed to disable addon: %s'% CHOICE)
                printstar()
                xbmc.executebuiltin('Notification(Problem with restoreaddon.py, Check log for details)')
                exit()        
    # delete folder
    try:
        shutil.rmtree(testpath)
        xbmc.sleep(300)
    except:
        printstar()
        print 'Problem with restoreaddon.py'
        print ('Cannot delete addon folder:%s'% testpath)
        print 'Sort this out manually'
        printstar()
        xbmc.executebuiltin('Notification(Problem with restoreaddon.py, Check log for details)')
        exit()
# copy backup into place
try:
    shutil.copytree(SOURCE, testpath)
    xbmc.sleep(300)
except:
    printstar()
    print 'Problem with restoreaddon.py'
    print ('Cannot copy addon folder:%s'% CHOSEN)
    print 'Sort this out manually'
    printstar()
    xbmc.executebuiltin('Notification(Problem with restoreaddon.py, Check log for details)')
    exit()
# update local addons, enable the addon if necessary, reload skin if necessary
xbmc.executebuiltin( 'UpdateLocalAddons' )
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHOSEN)
xbmc.sleep(300)
if not xbmc.getCondVisibility('System.HasAddon(%s)'% CHOSEN):
    printstar()
    print 'Problem with restoreaddon.py'
    print ('Cannot enable restored addon:%s'% CHOSEN)
    print 'Sort this out manually'
    printstar()
    xbmc.executebuiltin('Notification(Problem with restoreaddon.py, Check log for details)')
    exit()
else:
    print 'restoreaddon.py - all done'
    xbmc.executebuiltin('Notification(All, done)')
    exit()



