
# -*- coding: utf-8 -*-
# opens tv channel or guide groups via smashingfavourites and / or keymap.
import os
import os.path
import xbmc
import sys

# make sure dvbviewer is running - enable and wait if necessary
def enable():
    if not xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid":"pvr.dvbviewer","enabled":true}}')
        xbmc.sleep(200)
	
# make sure dvbviewer is not running - disable if necessary
def disable():
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')
	
# define terms... c = count
# f=0 for just pvr disabled f = 1 (value) if channels, f=2 (value) if guides, f=3 if radio, f=4 if recordings,
# f=5 if timers, f=6 if search, f=7 if recording / recorded files, f=8 for timeshift, f=9 for permanently enable, 
# f=10 for remove enable check.
# g = group number (value)... g=3 for last channel group / guide group

# define f
a = sys.argv[1]
f = int(a)

def terms():    
    b = sys.argv[2]
    c = 2
    g = int(b)

# f=3
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

# print stars to show up in log and error notification
def printstar():
	print "****************************************************************************"
    print "****************************************************************************"
	
def error():
    xbmc.executebuiltin('Notification(Check, smashingtv)')
    exit()
	
# open channel or guide windows	- f = 1,2
def opengroups():    
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
    if g >=1:		
	    xbmc.executebuiltin( "XBMC.Action(Select)" )
	    xbmc.executebuiltin( "XBMC.Action(Right)" )
	    xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )

# define file locations
def files():
    SOURCEFILE = os.path.join(xbmc.translatePath('special://userdata/favourites/smashingtv/enablefile'), "enablepvr.txt")
    TARGET = os.path.join(xbmc.translatePath('special://userdata/favourites/smashingtv'), "enablepvr.txt")

# permanentenable:	
# Copy pvrenable.txt to favourites/smashingtv folder as marker and enable pvr.dvbviewer - f=9
# check if SOURCEFILE exists - if not give an error message
# check if TARGET exists - if so give a notification 'already enabled'
# copy SOURCEFILE to TARGET, enable and close		
def permanentenable():
if not os.path.isfile(SOURCEFILE):
    printstar()
    print "smashingtv problem - check userdata/favourites/smashingtv/enablefile folder for missing pvrenable.txt"
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
    terms()
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


	

	
	


		
