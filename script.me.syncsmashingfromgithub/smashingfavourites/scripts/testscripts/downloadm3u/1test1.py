# -*- coding: utf-8 -*-

import xbmc
import urllib
import os

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
testfile = urllib.URLopener()

printstar()
print ('DOWNLOAD is %s'% DOWNLOAD)
print ('testfile is %s'% testfile)

testfile.retrieve("http://stream.fabiptv.com:25461/get.php?username=oqrfxtzg&password=m7q38iA3wE&type=m3u_plus&output=mpegts", DOWNLOAD)
xbmc.sleep(1000)
print 'check 1'
if os.path.exists(DOWNLOAD):
    xbmc.executebuiltin('Notification(Way, hey)')
else:
    xbmc.executebuiltin('Notification(Boo, hoo)')








