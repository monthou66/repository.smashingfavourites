#!/usr/bin/python
# -*- coding: utf-8 -*-
# startpvr.py

import xbmc
import os
import os.path
import sys
import shutil
import json

# define some places
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/'))
LOGPATH = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(LOGPATH, "kodi.log")
ENABLE = os.path.join(ADDONS, "script.me.pvrpermanentenable")
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")


def printstar():
    print "****************************************************************************"
    print "***************************************************************************"

def error():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Check, %s)'% thisaddon)
    exit()
	
def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
	
def checkpvrnotplaying():
    if (xbmc.getCondVisibility("Player.Playing")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')
        exit()
    if (xbmc.getCondVisibility("Pvr.IsPlayingTv")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()

def getarguments():
    # get arguments - to find which pvr addon to start - and which group?  Incorporate in SmashingTV
    global pvraddon, number, a, b, c
    pvraddon = sys.argv[1]			# which pvr addon - 'disable' = turn all off
                                    # if starts with 'refresh' clear database then load named addon - eg 'refreshpvr.dvbviewer
                                    # if pvraddon = 'refresh' just clear the database
									# 'permanent' = enable marker addon
									# 'temp' = disable marker addon
    number = len(sys.argv)
    print ('number is %d'% number)

    if len(sys.argv) > 2:
        a = sys.argv[2]     # channels or guides etc
    else:
        a = 'channels'
    if a == 0:
        a = 'channels'	
		
    if len(sys.argv) > 3:
        b = sys.argv[3]		# which group
        c = 2				# use to count to right group
    else:
        b = 0
        g = 0
        g = int(g)
			
def checkwantedpvr():
    global pvraddon
    if pvraddon == 'disable':
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            xbmc.executebuiltin("ActivateWindow(Home)")
            stoppvr()
            print ('%s check 16'% thisaddon)
            xbmc.executebuiltin('Notification(Live TV, has been disabled)')
            exit()
        else:
            xbmc.executebuiltin('Notification(Live TV, was not enabled)')
            exit()
    elif pvraddon == 'refresh':
        refresh()
        xbmc.executebuiltin('Notification(Live TV, refreshed)')
        exit()
#    elif pvraddon[:7] == 'refresh':
#        wantedpvr = pvraddon[0:8]
        # testslice
#        print ('wantedpvr is %s'% wantedpvr)
#        if xbmc.getCondVisibility('System.HasAddon(%s)'% wantedpvr):
#            refresh()
#            exit()
#        else:
#            pvraddon = wantedpvr
    # check for 'permanent' > set marker and quit
    elif pvraddon == 'permanent':
        permanentenable()
    elif pvraddon == 'temp':
        removepermanentcheck()
    else:
        printstar()
        print ('requested pvr addon is %s'% pvraddon)
        printstar()

def checkcurrentpvr():
    global STOP
    # check if the addon is already running - if not continue startup
	# check if any pvr running - if so stop.
    # then start pvraddon
    if not xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            stoppvr()
            xbmc.executebuiltin('Notification(Stopping, %s)'% STOP)
            refresh()
            exit()
        startpvr()
        xbmc.executebuiltin('Notification(Starting, %s)'% pvraddon)
        exit()		

def setf():
    global a, f
    if a in ["Channels", "channels", "Channel", "channel"]:
        f = 1
        f = int(f)
    elif a in ['Guide', 'guide']:
        f = 2
        f = int(f)
    elif a in ['Radio', 'radio']:
        radio()
    elif a in ['Recordings', 'recordings', 'Recorded', 'recorded', 'Recorded TV', 'recorded tv']:
        recordings()	
    elif a in ['Timers', 'timers']:
        timers()
    elif a in ['Search', 'search']:
        search()	
    elif a in ['Recorded files', 'Recorded Files', 'recorded files', 'recordedfiles', 'Files', 'files']:
        recordedfiles()	
    elif a in ['Timeshift', 'timeshift']:
        timeshift()
    else:
        f = 1
        f = int(f)
        printstar()
        print ('Problem with sys.argv1 in smashingtv. Script read a as %s but set f to 1' % a)
        printstar() 

def getchannelgroups():
    global CHANNELGROUPS, channelgroups, numb
    CHANNELGROUPS = []
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
    channelgroups = ret['result']['channelgroups']
    for channelgroup in channelgroups:
#        printstar()
#        print channelgroup
        chanstring = str(channelgroup)
        start = "u'label': u'"
        end = "'}"		
        group = (chanstring.split(start))[1].split(end)[0]
        CHANNELGROUPS.append(group)
#    print CHANNELGROUPS
    numb = len(CHANNELGROUPS)
    print ('There are %d channel groups' % numb)
    c = 0
    while c < numb:
        print CHANNELGROUPS[c]
        c = c + 1

def setg():
    global b, g, CHANNELGROUPS, channelgroups, numb
    c = 0
    g = 0
    print 'Now starting setg()'
    print CHANNELGROUPS
    print ('numb is %s'% numb)
    print ('b is %s'% b)
    while c < numb:
        GRP = CHANNELGROUPS[c]
        print ('CHANNELGROUPS[%d] is %s'% (c, GRP))
        if b == CHANNELGROUPS[c]:		
# try c + 1 ??????????
            g = c + 1
        c = c + 1
    if b in ["Choose", "choose", "Choose Group", "choose group"]:	
        g = 0
        print ('b read as %s' % b)
        print 'g set as 0 - choose group'
    print ('g is %s'% g)
    print ('The channel group is %s'% b)

# open channel or guide windows	- f = 1,2
def opengroups():
    global c, f, g	
    if f == 1:
	    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    elif f == 2: 
	    xbmc.executebuiltin('ActivateWindow(TVGuide)')	
    else:
	    xbmc.executebuiltin('Notification(Check, smashingtv)'); exit()
    xbmc.executebuiltin('SendClick(28)')
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
    # loop move down to correct group (if necessary)
    if g > 1:
	    while (c <= g):	
		    c = c + 1
		    xbmc.executebuiltin( "XBMC.Action(Down)" )
			
    # open group if not using 'choose' option.		
    if g >= 1:		
	    xbmc.executebuiltin( "XBMC.Action(Select)" )
	    xbmc.executebuiltin( "XBMC.Action(Right)" )
	    xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )
	
# permanentenable:
# Check if script.me.pvrpermanentenable is enabled.  If yes do nothing.
# If not - check if script.me.pvrpermanentenable exists in addons folder.
# If it does enable the script.  Finish
# If not copy the script into the addons folder, update local addons and enable it.  Done.		
def permanentenable():
    if not xbmc.getCondVisibility('System.HasAddon(script.me.pvrpermanentenable)'):
        if not os.path.exists(ENABLE):
            enablesource = os.path.join(SMASHINGFAVOURITES, "miscfiles", "addons", "myaddons", "markers", "script.me.pvrpermanentenable")
            shutil.copytree(enablesource, ENABLE)
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "script.me.pvrpermanentenable","enabled":true}}')		
        printstar()
        print "pvr has been permanently enabled"
        printstar()
    else:
        printstar()
        print "pvr was already permanently enabled"
        printstar()
    if xbmc.getCondVisibility('System.HasAddon(script.me.pvrpermanentenable)'):
        xbmc.executebuiltin('Notification(Live TV is, permanently enabled)')
        exit()
    else:
        xbmc.executebuiltin('Notification(Something, went wrong)')
        printstar()
        print ('%s > permanentenable did not work correctly'% thisaddon)
        printstar()
        error()

# removepermanentpvrmarker
# Disable script.me.pvrpermanentenable if f=10
def removepermanentcheck():
    if xbmc.getCondVisibility('System.HasAddon(script.me.pvrpermanentenable)'):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "script.me.pvrpermanentenable","enabled":false}}')
#        printstar()
#        print "pvr is not permanently enabled"
#        printstar()
    if not xbmc.getCondVisibility('System.HasAddon(script.me.pvrpermanentenable)'):		
        xbmc.executebuiltin('Notification(Live TV will be, turned off when idle)')
        exit()
    else:
        xbmc.executebuiltin('Notification(Something, went wrong)')
        printstar()
        print ('%s > removepermanentenable did not work correctly'% thisaddon)
        printstar()
        error()	

def radio():
    xbmc.executebuiltin('ActivateWindow(Radio)')
    exit()	

# f=4
def recordings():
    xbmc.executebuiltin('ActivateWindow(tvrecordings)')
    exit()	

# f=5	
def timers():
    xbmc.executebuiltin('ActivateWindow(tvtimers)')
    exit()

# f=6	
def search():
    xbmc.executebuiltin('ActivateWindow(tvsearch)')
    exit()
	
# pvr can be disabled for recorded files - f=7
def recordedfiles():
    xbmc.executebuiltin('Videos,smb://SourceTVRecordings/,return')
    exit()
	
# pvr can be disabled for timeshift files - f=8
def timeshift():
    xbmc.executebuiltin('Videos,smb://SourceTVRecordings/,return')
    exit()	


def checkstart():
    global LOGFILE, starttime, length
    startline = 'not found'
    length = 0
    with open(LOGFILE) as f:
        for line in f:
            length = length + 1
    printstar()
    print ('There are %s lines in the log'% length)
    printstar()
	
    with open(LOGFILE) as f:
        lines = f.readlines()
        w = length
        countback = 0
        while countback < 500:
            startline = lines[w]
            if ('%s has started'% thisaddon) in startline:
                startlog = w + 1
                printstar()
                print ('startline is %s'% startline)
                print ('This is line %d'% startlog)
                printstar()
                countback = 5000
            countback = countback + 1
            w = w - 1
    if not countback == 5001:
        printstar()
        print ('startline not found.  %s will close now.'% thisaddon)
        error()
        exit()
    else:
        xbmc.executebuiltin('Notification(startline is line, %s)'% startlog)
	
	
# lose this	
def checkstartold():
    # check the log to see the time the addon starts
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
    global ADDONS, STOP
    print ('%s check 10'% thisaddon)
    # quick check - is pvr active? are dvbviewer / iptvsimple active?  Then check the rest.
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        xbmc.executebuiltin("ActivateWindow(Home)")
        xbmc.sleep(300)
        print ('%s check 11'% thisaddon)	
        if xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):
            print ('%s check 12'% thisaddon)
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')            
            print ('%s check 13'% thisaddon)
#			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')
            STOP = 'dvbviewer'
        if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')
#            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')
            STOP = 'iptvsimple'
	# check if any other pvr addons are installed.  If yes stop them
    print ('%s check 14'% thisaddon)
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        PATHADDONS = [d for d in os.listdir(ADDONS) if os.path.isdir(os.path.join(ADDONS, d))]
        ALTADDONS = [d for d in os.listdir(ALTERNATE) if os.path.isdir(os.path.join(ALTERNATE, d))]
        ALLADDONS = PATHADDONS + ALTADDONS
        ALLPVR = [s for s in ALLADDONS if "pvr." in s]
        printstar()
        print ('ALLPVR is %s'% ALLPVR)	
        printstar()		
        x = len(ALLPVR)
        y = 0
        while y < x:
            CHECK = ALLPVR[y]
            if xbmc.getCondVisibility('System.HasAddon(%s)'% CHECK):
                print ('disabling %s'% CHECK)
                STOP = CHECK
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s","enabled":false}}'% CHECK)
                xbmc.sleep(1000)
                printstar()
                print 'check 1'
                if not xbmc.getCondVisibility('System.HasPVRAddon'):
                    y = x
                    printstar()
                    print 'check 2'				
#                    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% pvraddon)
            y = y + 1				
    printstar()
    print ('%s check 15'% thisaddon)

	
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
#    if not pvraddon == 'disable':
#        xbmc.executebuiltin('Notification(Live TV, is starting)')
#    xbmc.sleep(2000)		

def startpvr():	
    global pvraddon	
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
            error()
            exit()
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% pvraddon)
    printstar()
    print 'check 4'	
	
def checkready():
    xbmc.sleep(10000)

def realcheckready():
    # check the log for 'radio channel groups loaded' after the script started - if that appears it's safe to switch to a pvr window
    global LOGFILE, starttime
    found = 'false'
    h = 1
    while h <= 49:
        with open(LOGFILE) as f:
            lines = f.readlines()
            w = 1
            while w < 500:
                finishline = lines[-w]
                if ('%s has started'% thisaddon) in finishline:
                    xbmc.sleep(300)
                    w = 500				
                elif 'radio channel groups loaded' in finishline:
                    printstar()
                    print ('finishline is %s'% finishline)
                    printstar()
                    found = 'true'
                    w = 500
                w = w + 1
#                print ('w is %s'% w)
        if found == 'false':
            h = h + 1
            printstar()
#            print ('h is %s'% h)
        else:
            h = 50
#            h = h + 20
            printstar()
            print ('h is %s'% h)
    if found == 'false':
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
#    xbmc.executebuiltin('ActivateWindow(TVChannels)')
#    exit()	
		

# Get on with it.
print 'check 1'
startaddon()
print ('%s check 2'% thisaddon)
checkpvrnotplaying()
print ('%s check 3'% thisaddon)
# checkstart()

getarguments()
print ('%s check 4'% thisaddon)
checkwantedpvr()
print ('%s check 5'% thisaddon)
checkcurrentpvr()
print ('%s check 6'% thisaddon)
# follow it through gets to end of startpvr() if required - chosen pvr is running, now look at window.
# checkready()

setf()

getchannelgroups()

setg()

opengroups()

exit()


	
