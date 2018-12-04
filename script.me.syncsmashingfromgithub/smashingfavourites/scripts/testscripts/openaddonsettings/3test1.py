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

def fail()
    print 'running fail()'
    print message
    xbmc.executebuiltin('Notification(Big, fail)')
    exit()

def getfoldername()
    global FolderName, message
    print 'running getfoldername()'
    c = 0
    while c < 15:
        FolderName = xbmc.getInfoLabel('Container.FolderName')
        if not FolderName = "":
            c = 1000
        else:
            xbmc.sleep(300)
        c = c + 1
    if c < 1000:
        message = 'FolderName not found'
        fail()
        
# open addons window
xbmc.executebuiltin('ActivateWindow(10040)')        #works
xbmc.sleep(300)

# get foldername

# Add-on browser
# My add-ons
# PVR clients

getfoldername()
if not FolderName == 'PVR clients':
c = 0
while c < 10:
    if FolderName == 'PVR clients':
        c = 1000
    if FolderName == 'Add-on browser':
        wanted = 'My add-ons'
        openfolder()
    elif FolderName == 'My add-ons':
        wanted = 'PVR clients'
        openfolder()
    else:
    

# get CurrentItem
c = 0
while c < 15:
    CurrentItem = xbmc.getInfoLabel('System.CurrentControl')
    if not CurrentItem = "":
        c = 1000
    else:
        xbmc.sleep(300)
    c = c + 1
if c < 1000:
    message = 'CurrentItem not found'
    fail()
    

content = xbmc.getInfoLabel('Container.Content')
numitems = xbmc.getInfoLabel('Container.NumItems ')
position = xbmc.getInfoLabel('Container.Position')
numitems = int(numitems)

print ('FolderName is %s'% FolderName)
print ('CurrentItem is %s'% CurrentItem)
print ('content is %s'% content)
print ('numitems is %d'% numitems)
print ('position is %s'% position)

offset = 0
c = 0
size = numitems + 1
while c < size:
    print ('c = %d'% c)
    check = xbmc.getInfoLabel('Container.ListItem(%d).Label'% c)
    print ('check = %s'% check)
    if 'PVR clients' in check:
        offset = c
        print ('offset = %s'% offset)
        c = 1000
    c = c + 1
if c > 999:
    print ('offset is %d'% offset)
else:
    print 'no idea what the offset is'

print 'all done'
exit()

xbmc.executebuiltin( "XBMC.Action(Up)")
xbmc.sleep(300)
CurrentItem = xbmc.getInfoLabel('System.CurrentControl')
print ('CurrentItem is now %s'% CurrentItem)

exit()
if not CurrentItem == '[PVR clients]':
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
    CurrentItem = xbmc.getInfoLabel('System.CurrentControl')
    print ('CurrentItem is %s'% CurrentItem)
    if CurrentItem == '[My add-ons]':
        xbmc.executebuiltin( "XBMC.Action(Select)")
        xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
    
    xbmc.executebuiltin( "XBMC.Action(Up)")
    xbmc.executebuiltin( "XBMC.Action(Up)")
    xbmc.executebuiltin( "XBMC.Action(Up)")
    xbmc.executebuiltin( "XBMC.Action(Up)")
    xbmc.executebuiltin( "XBMC.Action(Up)")
    xbmc.executebuiltin( "XBMC.Action(Select)")


message = ('All, done')
xbmc.executebuiltin('Notification(%s)'% message)
exit()
# responses
# group = Group: All channels
# group =