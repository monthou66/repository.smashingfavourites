# -*- coding: utf-8 -*-

import xbmc
import urllib
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')

# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
DOWNLOAD = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "downloadedfab.m3u")
OLDFILE = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "oldfab.m3u")
testfile = urllib.URLopener()
uksports = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "uksports.m3u")
out = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "merged.m3u")
oldout = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "oldmerged.m3u")

def mergem3us():
    global USERDATA, SMASHINGFAVOURITES, DOWNLOAD, out, oldout, uksports
    if os.path.isfile(out):
        os.rename(out, oldout)
        print 'check 4'
    else:
        print 'check 5'

    f = open(DOWNLOAD, 'r')
    text = f.read()
    f.close()
    with open(out, "a") as myfile:
        myfile.write(text)

    f = open(uksports, 'r')
    text = f.read()
    f.close()
    with open(out, "a") as myfile:
        myfile.write(text.replace('#EXTM3U#','').replace('#EXTM3U',''))
    xbmc.executebuiltin('Notification(m3us have been, merged)')

printstar()
print ('DOWNLOAD is %s'% DOWNLOAD)
print ('testfile is %s'% testfile)
print ('OLDFILE is %s'% OLDFILE)
if os.path.exists(OLDFILE):
    os.remove(OLDFILE)

if os.path.isfile(DOWNLOAD):
    os.rename(DOWNLOAD, OLDFILE)
    print 'check 1'
else:
    print 'check 2'

testfile.retrieve("http://stream.fabiptv.com:25461/get.php?username=oqrfxtzg&password=m7q38iA3wE&type=m3u_plus&output=mpegts", DOWNLOAD)
xbmc.sleep(1000)
print 'check 3'
if os.path.exists(DOWNLOAD):
    xbmc.executebuiltin('Notification(Way, hey)')
else:
    xbmc.executebuiltin('Notification(Boo, hoo)')

mergem3us()
	








