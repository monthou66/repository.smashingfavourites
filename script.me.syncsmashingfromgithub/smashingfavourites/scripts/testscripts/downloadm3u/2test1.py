# -*- coding: utf-8 -*-

import xbmc
import urllib2
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


printstar()
print ('DOWNLOAD is %s'% DOWNLOAD)

response = urllib2.urlopen('http://stream.fabiptv.com:25461/get.php?username=oqrfxtzg&password=m7q38iA3wE&type=m3u_plus&output=mpegts')
html = response.read()
xbmc.sleep(1000)
print html


print 'check 1'
if os.path.isfile(DOWNLOAD):
    xbmc.executebuiltin('Notification(Way, hey)')
else:
    xbmc.executebuiltin('Notification(Boo, hoo)')










