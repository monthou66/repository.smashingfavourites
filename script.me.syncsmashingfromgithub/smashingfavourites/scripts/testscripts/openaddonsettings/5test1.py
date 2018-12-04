#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc

print 'running test1.py'
    
def finish():
    print 'running finish()'
    print message
    if not screenmessage == 'not set':
        xbmc.executebuiltin('Notification(%s)'% screenmessage)            
    exit()    

def findaddon():
    global FolderPath, message, screenmessage
    print 'running findaddon()'
    print ('wanted is %s'% wanted)
    numitems = xbmc.getInfoLabel('Container.NumItems')
    if numitems == "":
        d = 0
        while d < 5:
            xbmc.sleep(300)
            numitems = xbmc.getInfoLabel('Container.NumItems')
            if not numitems == "":
                d = 1000
            else:
                d = d + 1
        if d < 1000:
            message = 'could not find numitems'
            screenmessage = 'No, go'
            finish()        
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
        message = ('could not find offset for'% wanted)
        screenmessage = 'No, go'
        finish()
    c = 0
    while c < offset:
        xbmc.executebuiltin("XBMC.Action(Down)")
#        xbmc.executebuiltin("ActivateScreensaver()") 
        c = c + 1
    if opensettings == 'true':
        xbmc.executebuiltin( "XBMC.Action(Select)" )
        if configure == 'true':
            xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
            xbmc.executebuiltin( "XBMC.Action(Select)" )
    message = 'Did it work then?'        
    print 'leaving openfolder()'
   
# starty start
screenmessage = 'not set'
pvrid = 'not set'
#opensettings = 'false'
opensettings = 'true'
configure = 'false'
#configure = 'true'

# assume addonid - will come from argument
pvrid = 'pvr.dvbviewer'
#pvrid = 'pvr.iptvfree'

if xbmc.getCondVisibility('System.HasAddon(%s)' % pvrid):
    if configure == 'true':
        xbmc.executebuiltin('Addon.OpenSettings(%s)'% pvrid)
        message = 'done with xbmcaddon'
        screenmessage = 'fancypants, way'
        finish()
        
# if we're still here do it the other way...
# open window
xbmc.executebuiltin('ActivateWindow(AddonBrowser,"addons://user/xbmc.pvrclient",return)')
# move to addon

if not pvrid == 'not set':
    pvrname = xbmc.getInfoLabel('System.AddonTitle(%s)'% pvrid)
    screenmessage = ('pvrname is, %s'% pvrname)
    xbmc.executebuiltin('Notification(%s)'% screenmessage)
    wanted = pvrname
    findaddon()


message = 'stopping test1.py'
finish()