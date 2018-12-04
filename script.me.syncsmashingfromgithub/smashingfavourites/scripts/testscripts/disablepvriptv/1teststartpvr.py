#!/usr/bin/python
# -*- coding: utf-8 -*-
# startpvr.py

import xbmc
import os

# define some places
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/'))
LOGPATH = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(LOGPATH, "kodi.log")

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"

def checkstart():
    global LOGFILE, starttime
    startline = 'not found'
    with open(LOGFILE) as f:
        lines = f.readlines()
        w = 1
        while w < 100:
            startline = lines[-w]
            if ('%s has started'% thisaddon) in startline:
                printstar()
                print ('startline is %s'% startline)
                printstar()
                w = w + 100
            w = w + 1
    if startline == 'not found':
        printstar()
        print ('startline not found.  %s will close now.'% thisaddon)
        exit()

    h = startline[:2]
    m = startline[3:5]
    s = startline[6:8]
    # printstar()
    # print ('h is %s'% h)
    # print ('m is %s'% m)
    # print ('s is %s'% s)
    # printstar()
    # exit()
    h = int(h)
    m = int(m)
    s = int(s)
    # get time in seconds
    starttime = (h*3600) + (m*60) + s	

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

	
def refresh():
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
    if not pvraddon == 'disable':
        xbmc.executebuiltin('Notification(Live TV, is starting up)')
    xbmc.sleep(2000)	
	
	
def startpvr():	
#    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":true}}')	
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% pvraddon)	
    printstar()
    print 'check 4'	

def checkready():
    global LOGFILE, starttime
    finishline = 'not found'
    h = 1
    while h <= 20:
        with open(LOGFILE) as f:
            lines = f.readlines()
            w = 1
            while w < 500:
                finishline = lines[-w]
                if 'radio channel groups loaded' in finishline:
                    printstar()
                    print ('finishline is %s'% finishline)
                    printstar()
                    w = 500
                w = w + 1
        if finishline == 'not found':
            h = h + 1
        else:
            h = h + 20
    if finishline == 'not found':
        printstar()
        print ('finishline not found. %s will stop'% thisaddon)
        printstar()		
        exit()				
    h = finishline[:2]
    m = finishline[3:5]
    s = finishline[6:8]
    # printstar()
    # print ('h is %s'% h)
    # print ('m is %s'% m)
    # print ('s is %s'% s)
    # printstar()
    # exit()
    h = int(h)
    m = int(m)
    s = int(s)
    # get time in seconds
    finishtime = (h*3600) + (m*60) + s
    timetaken = finishtime - starttime		
    printstar()
    print ('starttime is %d'% starttime)
    print ('starttime is %d'% starttime)
    print ('timetaken is %d'% timetaken)
    printstar()
    if starttime > finishtime:
        printstar()
        print ('starttime > finishtime: %s will exit'% thisaddon)		
        printstar()
    xbmc.sleep(300)
    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    exit()	
		

# Get on with it.

thisaddon = sys.argv[0]
printstar()
print ('%s has started'% thisaddon)
xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
checkstart()

# get arguments - to find which pvr addon to start - and which group?  Incorporate in SmashingTV
pvraddon = sys.argv[1]			# which pvr addon - 'disable' = turn all off
                                # if starts with 'refresh' clear database then load named addon - eg 'refreshpvr.dvbviewer
                                # if pvraddon = 'reset' just clear the database
number = len(sys.argv)
print ('number is %d'% number)


if len(sys.argv) > 2:
    a = sys.argv[2]     # channels or guides etc
if len(sys.argv) > 3:
    b = sys.argv[3]		# which group
    c = 2				# use to count to right group
else:
    b = 0	

if not pvraddon == 'disable':	
    if pvraddon == 'refresh':
        refresh()
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
    refresh()

if pvraddon == 'disable':
    xbmc.executebuiltin('Notification(PVR, disabled)')
    exit()
	
startpvr()
checkready()
changescreen()


exit()
	
