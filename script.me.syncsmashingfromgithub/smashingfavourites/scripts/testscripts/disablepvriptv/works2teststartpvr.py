#!/usr/bin/python
# -*- coding: utf-8 -*-
# startpvr.py

import xbmc
import os

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"

thisaddon = sys.argv[0]
printstar()
print ('%s has started'% thisaddon)
xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
	
# define some places
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/'))

def stoppvr():
    global ALLPVR
    x = len(ALLPVR)
    y = 0
    while y < x:
        CHECK = ALLPVR[y]
        if xbmc.getCondVisibility('System.HasAddon(%s)'% CHECK):
            print ('disabling %s'% CHECK)
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s","enabled":false}}'% CHECK)
            xbmc.sleep(1000)
            printstar()
            print 'check 1'
            if not xbmc.getCondVisibility('System.HasPVRAddon'):
                y = x
                printstar()
                print 'check 2'				
#                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% pvraddon)
        y = y + 1				
    printstar()
    print 'check 3'
# refresh the pvr database	
    xbmc.executebuiltin("ActivateWindow(10021)")
    xbmc.executebuiltin( "XBMC.Action(Right)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Select)" )
    xbmc.executebuiltin('SendClick(11)')
    xbmc.executebuiltin("ActivateWindow(Home)")
    xbmc.sleep(2000)	
	
	
	
#    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":true}}')	
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% pvraddon)	
    printstar()
    print 'check 4'	
    exit()
	
	

# get arguments - to find which pvr addon to start - and which group?  Incorporate in SmashingTV
pvraddon = sys.argv[1]			# which pvr addon - 'disable' = turn all off

number = len(sys.argv)
print ('number is %d'% number)


if len(sys.argv) > 2:
    a = sys.argv[2]     # channels or guides etc
if len(sys.argv) > 3:
    b = sys.argv[3]		# which group
    c = 2				# use to count to right group
else:
    b = 0	
	
print ('requested pvr addon is %s'% pvraddon)
	
# check if the addon is already running - if not continue startup
if xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
#    forgetalltherestofthisrubbish()
    print 'addon already running'
else:
    print ('%s is not running'% pvraddon)

# check system has the addon in the argument - otherwise generate a notification
PATH = os.path.join(ADDONS, pvraddon)
ALTPATH = os.path.join(ALTERNATE, pvraddon)
print ('PATH is %s'% PATH)
print ('ALTPATH is %s'% ALTPATH)
if not os.path.exists(PATH):
    if os.path.exists(ALTPATH):
        PATH = ALTPATH
    else:
        printstar()
        print ('Tried to start %s but the addon is not installed.'% pvraddon)
        printstar()
        xbmc.executebuiltin('Notification(%s, is not installed)'% pvraddon)

# check if any other pvr addons are installed.  If yes stop them
if xbmc.getCondVisibility('System.HasPVRAddon'):
    PATHADDONS = [d for d in os.listdir(ADDONS) if os.path.isdir(os.path.join(ADDONS, d))]
    ALTADDONS = [d for d in os.listdir(ALTERNATE) if os.path.isdir(os.path.join(ALTERNATE, d))]
    ALLADDONS = PATHADDONS + ALTADDONS
    ALLPVR = [s for s in ALLADDONS if "pvr." in s]
    printstar()
    print ('ALLPVR is %s'% ALLPVR)
    stoppvr()




# start the addon
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% pvraddon)


exit()
if not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
    if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):	
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":false}}')
        xbmc.sleep(1000)
    if xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):		
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')	
        xbmc.sleep(10000)
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":true}}')
    xbmc.sleep(10000)
xbmc.executebuiltin('ActivateWindow(TVChannels)')	
