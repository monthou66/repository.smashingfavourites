#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

print 'running test1.py'

#xbmcaddon.Addon('pvr.dvbviewer').openSettings()
#thingy = 'pvr.iptvsimple'
# thingy = 'pvr.dvbviewer'
#xbmc.executebuiltin('Addon.OpenSettings(%s)'% thingy)
# Addon.OpenSettings('pvr.dvbviewer')
# xbmcaddon.Addon().openSettings() 
# xbmcaddon.Addon('%s'% thingy).openSettings() 

# xbmc.executebuiltin('ActivateWindow(addons://user/pvr/pvr.dvbviewer)') # no go
#xbmc.executebuiltin('ActivateWindow(addons://user/xbmc.pvrclient)') # no go
# xbmc.executebuiltin('ActivateWindow(videodb://movies/titles/)') # no go
# xbmc.executebuiltin('Addon.OpenSettings(pvr.dvbviewer)') # works

def fail():
    print 'running fail()'
#    xbmc.executebuiltin("ReloadSkin()")
#    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.Select", "id": 1}')
    print message
    xbmc.executebuiltin('Notification(Big, fail)')
    exit()
    
def finish():
    print 'running finish()'
#    xbmc.executebuiltin("ReloadSkin()")
#    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.Select", "id": 1}')
    print message
    xbmc.executebuiltin('Notification(All, done)')

    print ('tv = %s'% tv)    
    if tv == 'true':
        xbmc.executebuiltin("XBMC.Action(FullScreen)")
            
    exit()

def getfolderpath():
    global FolderPath, message
    print 'running getfolderpath()'
    c = 0
    while c < 15:
        FolderPath = xbmc.getInfoLabel('Container.FolderPath')
        if not FolderPath == "":
            c = 1000
        else:
            xbmc.sleep(300)
        c = c + 1
    if c < 1000:
        message = 'FolderPath not found'
        fail()
    else:
        print ('FolderPath is %s'% FolderPath)

def openfolder():
    global FolderPath, message
    print 'running openfolder()'
    print ('wanted is %s'% wanted)
    numitems = xbmc.getInfoLabel('Container.NumItems ')
    numitems = int(numitems)
    offset = 0
    c = 0
    size = numitems + 1
    while c < size:
        print ('c = %d'% c)
        check = xbmc.getInfoLabel('Container.ListItem(%d).Label'% c)
        print ('check = %s'% check)
        if wanted in check:
            offset = c
            print ('offset = %s'% offset)
            c = 1000
        c = c + 1
    if c > 999:
        print ('offset is %d'% offset)
    else:
        print 'no idea what the offset is'
        message = ('could not find offset in %s foldr'% FolderPath)
        fail()
    c = 0
    while c < offset:
        xbmc.executebuiltin("XBMC.Action(Down)")
#        xbmc.executebuiltin("ActivateScreensaver()") 
        c = c + 1
    xbmc.executebuiltin( "XBMC.Action(Select)" )
#    xbmc.executebuiltin("ActivateScreensaver()") 

#    xbmc.sleep(300)
#    print ('FolderPath was %s'% FolderPath)
#    FolderPath = xbmc.getInfoLabel('Container.FolderPath')    
#    print ('FolderPath is now %s'% FolderPath)        
    print 'leaving openfolder()'
    
def upalevel():
    global FolderPath, message
    print 'running upalevel()'
    xbmc.executebuiltin( "XBMC.Action(Back)" )
    
#    xbmc.sleep(300)
#    print ('FolderPath was %s'% FolderPath)
#    FolderPath = xbmc.getInfoLabel('Container.FolderPath')    
#    print ('FolderPath is now %s'% FolderPath)
    print 'leaving upalevel()'    

#xbmc.executebuiltin("ActivateScreensaver()")    

# starty start

pvrid = 'pvr.dvbviewer'
pvrname = xbmc.getInfoLabel('System.AddonTitle(%s)'% pvrid) 

tv = 'false'
test = xbmc.getCondVisibility("Pvr.IsPlayingTv")
print ('test is %s'% test)
if test == '1':
    tv == 'true' 
print ('tv = %s'% tv)
tv = 'true'
print ('tv = %s'% tv)

    
# open addons window
xbmc.executebuiltin('ActivateWindow(10040)')        #works
#xbmc.executebuiltin("ActivateScreensaver()") 
xbmc.sleep(300)

# get folderpath ( want addons://user/xbmc.pvrclient)

getfolderpath()
x = 0
while x < 10:
    xbmc.sleep(200)
    print ('checking stuff - %d'% x)
    print ('FolderPath was %s'% FolderPath)    
    FolderPath = xbmc.getInfoLabel('Container.FolderPath')
    print ('FolderPath is now %s'% FolderPath)    
    if not FolderPath == 'addons://user/xbmc.pvrclient':
        if FolderPath == 'addons://user/':
            wanted = 'PVR clients'
            openfolder()
        elif FolderPath == 'addons://':
            wanted = 'My add-ons'
            openfolder()
        else:
            upalevel()
    else:
        xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
        x = 10
    x = x + 1
print 'Doney done done'
message = ('All, done')
finish()
    
    
    
# get CurrentItem
c = 0
while c < 15:
    CurrentItem = xbmc.getInfoLabel('System.CurrentControl')
    if not CurrentItem == "":
        c = 1000
    else:
        xbmc.sleep(300)
    c = c + 1
if c < 1000:
    message = 'CurrentItem not found'
    fail()
else:
    message = 'Hopefully looking at pvrclients?'
    finish()
    
