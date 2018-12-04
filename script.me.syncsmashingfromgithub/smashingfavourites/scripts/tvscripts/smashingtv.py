
# -*- coding: utf-8 -*-
# opens tv channel or guide groups via smashingfavourites and / or keymap.
import os
import os.path
import xbmc
import sys
import json

# make sure dvbviewer is running - enable and exit script - next press starts the wanted option
def enable():
    if not xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid":"pvr.dvbviewer","enabled":true}}')
#        xbmc.sleep(200)
        exit()
		
# make sure dvbviewer is not running - disable if necessary
def disable():
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')

# print stars to show up in log and error notification
def printstar():
    print "****************************************************************************"
    print "***************************************************************************"
	
def error():
    xbmc.executebuiltin('Notification(Check, smashingtv)')
    exit()
	
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
#    printstar()







	
# define terms... c = count
# f=0 for just pvr disabled f = 1 (value) if channels, f=2 (value) if guides, f=3 if radio, f=4 if recordings,
# f=5 if timers, f=6 if search, f=7 if recording / recorded files, f=8 for timeshift, f=9 for permanently enable, 
# f=10 for remove enable check.
# g = group number (value)... g=3 for last channel group / guide group

# or... accept name input for a and b:	

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









def setgold():
    global b, g
    if b in ["All", "all", "All channels", "All Channels", "all channels", "allchannels"]:	
        g = 1
        print ('b read as %s' % b)
        print 'g set as 1'
    elif b in ["Free", "free"]:
        g = 2
    elif b in ["Sport", "sport"]:
        print ('b read as %s' % b)
        print 'g set as 3'	
        g = 3
    elif b in ["Interactive", "interactive"]:
        print ('b read as %s' % b)
        print 'g set as 4'	
        g = 4
    elif b in ['Kids', 'kids']:
        g = 5
    elif b in ['Music', 'music']:
        g = 6
    elif b in ['International', 'international']:
        g = 7
    elif b in ['News', 'news']:
        g = 8
    elif b in ['Films', 'films']:
        g = 9
    elif b in ['Entertainment', 'entertainment']:
        g = 10
    elif b in ['Sky', 'sky']:
        g = 11
    elif b in ['Documentary', 'documentary', 'Doc', 'doc', 'Docs', 'docs']:
        g = 12
    else:
        g = 0	
        printstar()
        print ('Problem with sys.argv2 in smashingtv. Script read b as %s but set g to zero' % b)
        printstar() 		
	g = int(g)	
	
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
		

# define file locations
def files():
    SOURCEFILE = os.path.join(xbmc.translatePath('special://masterprofile/smashing/smashingfavourites/options/tv/enablefile'), "enablepvr.txt")
    TARGET = os.path.join(xbmc.translatePath('special://masterprofile/smashing/smashingfavourites/options/tv'), "enablepvr.txt")

# permanentenable:	
# Copy pvrenable.txt to smashingfavourites/options/tv folder as marker and enable pvr.dvbviewer - f=9
# check if SOURCEFILE exists - if not give an error message
# check if TARGET exists - if so give a notification 'already enabled'
# copy SOURCEFILE to TARGET, enable and close		
def permanentenable():
    if not os.path.isfile(SOURCEFILE):
        printstar()
        print "smashingtv problem - check masterprofile/smashing/smashingfavourites/options/tv/enablefile folder for missing pvrenable.txt"
        printstar()
        error()
    if os.path.isfile(TARGET):
        xbmc.executebuiltin('Notification(PVR is, already enabled)')
        enable()
        exit()
    else:
        shutil.copy(SOURCEFILE, TARGET)
        xbmc.executebuiltin('Notification(PVR is, permanently enabled)')
        enable()
        exit()	
	
#removepermanentcheck
# Remove pvrenable.txt from favourites/smashingtv folder f=10
def removepermanentcheck():
    if not os.path.isfile(TARGET):	
        xbmc.executebuiltin('Notification(No PVR, lock found)')
        disable()
        exit()
    else:
        os.remove(TARGET)
        xbmc.executebuiltin('Notification(PVR, unlocked)')
        disable()
        exit()
	
# Get on with it...

# define stuff
a = sys.argv[1]			# channels or guides etc
if len(sys.argv) > 1:
    b = sys.argv[2]		# which group
    c = 2				# use to count to right group
else:
    b = 0

if a.isdigit():
    f = int(a)
else:
    setf()

if b.isdigit():
    g = int(b)
else:
    getchannelgroups()
    setg()

# disable or enable pvr.dvbviewer, exit if necessary, exit and print message if f is out of range
if f == 0:
    disable()
    exit()
elif f == 7 or f == 8:
	disable()	
elif f > 10 or f < 0:
    printstar()
    print "smashingtv exited 'cos f is out of range"
    print "f is ",f
    printstar()
    error()
else:
    enable()
if f == 1 or f == 2:
    opengroups()	
elif f == 3:
    radio()
elif f == 4:
    recordings()
elif f == 5:
    timers()
elif f == 6:
    search()
elif f == 7:
    recordedfiles()
elif f == 8:
    timeshift()
elif f == 9:
    permanentenable()
    enable()
elif f == 10:
    removepermanentcheck()
    disable()
else:
    printstar()
    print "smashingtv exited 'cos sumfink went rong"	
    printstar()
    error()
