# -*- coding: utf-8 -*-
# get masterprofile
import xbmc
import os
from os import listdir
import socket
import sys
import xbmcgui

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"     
	
def setspecs():
    if not os.path.exists(SMASHINGSPECIFICS):
        os.mkdir(SMASHINGSPECIFICS)
    if not os.path.exists(SMASHHOST):
        os.mkdir(SMASHHOST)
    setupfile()
	
def redosettings():
    os.remove(SETTS)
    setupfile()
	
def setupfile():
    xbmcgui.Dialog().ok('     Setting defaults', '     Unplug all usb drives EXCEPT the',  '     Libreelec boot drive before continuing', 'Click OK when ready.')
    volumes = []
    volumes = listdir('/media')
    num = len(volumes)
    print ('num is %d'% num)
#    num = str(num)
#    print ('num is %s'% num)
#    windows
    win10 = xbmcgui.Dialog().yesno("Are you running Windows 10","on this machine?")
    if win10:
        winver = '10'
    else:
        win7 = xbmcgui.Dialog().yesno("Are you running Windows7","on this machine?")
        if win7:
            winver = '7'
        else:
            xbmcgui.Dialog().ok('     No operating system has been selected.', '     Action cancelled.')
            exit()
			
    with open(SETTS, "w") as text_file:
        text_file.write("%d volumes found in media \n" % num)
        text_file.write("windows version is: \n")
        text_file.write(winver)
#    open(SETTS, 'w')
#    file.write(num)
    xbmcgui.Dialog().ok('     Settings have been saved.', '     Run the script again to boot into windows.')
    exit()
	
# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGSPECIFICS = os.path.join(USERDATA, "smashing", "smashingspecifics")
vols = []
vols = listdir('/media')
num = len(vols)
host = socket.gethostname()
SMASHHOST = os.path.join(SMASHINGSPECIFICS, host)
SETTS = os.path.join(SMASHHOST, "rebootwindows.txt")

if not os.path.exists(SETTS):
    setspecs()

if len(sys.argv) == 2:
    function = sys.argv[1]
    if function == 'redo':
        redosettings()
		
# read SETTS - if current number of drives is bigger than in SETTS use 2,0 to start windows.
#with open(SETTS, 'r') as f:
#    line1 = f.readline()
#    defaultdrives = line1[:1]
#    defaultdrives = int(defaultdrives)
#f.close()

#*****************************************************************************

f=open('SETTS')
lines=f.readlines()
line1 = lines[0]
defaultdrives = line1[:1]
windowsversion = lines[2]
f.close() 

#*****************************************************************************

if num > defaultdrives:
    print 'num > defaultdrives'
elif num == defaultdrives:
    print'num == defaultdrives'
	
printstar()
print "test9.py has just been started"
print vols
print ('There are %d volumes in /media' % num)
print ('Hostname is %s' % host)
print ('line1 is %s'% line1)
print ('defaultdrives is %d'% defaultdrives)
printstar()
# xbmc.executebuiltin('Notification(test4.py, started)')




