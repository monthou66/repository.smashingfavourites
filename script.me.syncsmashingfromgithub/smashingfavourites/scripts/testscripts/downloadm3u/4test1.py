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
IPTVFOLDER = os.path.join(SMASHINGTEMP, "iptv")
DOWNLOADFIRSTFOLDER = os.path.join(IPTVFOLDER, "downloadfirst")
FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, 'fabiptv.m3u')
DOWNLOADRESTFOLDER = os.path.join(IPTVFOLDER, "downloadmore")
OLDFOLDER = os.path.join(IPTVFOLDER, "oldfiles")
OLDFILE = os.path.join(OLDFOLDER, 'fabiptv.m3u')
IPTVFILE = urllib.URLopener()
APPENDFOLDER =  os.path.join(IPTVFOLDER, "appendfiles")
# uksports = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "uksports.m3u")
out = os.path.join(IPTVFOLDER, "merged.m3u")
oldout = os.path.join(OLDFOLDER, "merged.m3u")

def mergefiles():
    global USERDATA, SMASHINGFAVOURITES, IPTVFOLDER, DOWNLOADFIRSTFOLDER, FIRSTFILE, DOWNLOADRESTFOLDER, OLDFOLDER, OLDFILE
    global IPTVFILE, APPENDFOLDER, out, oldout
    if os.path.isfile(oldout):
        os.remove(oldout)	
    if os.path.isfile(out):
        os.rename(out, oldout)
        print 'merged.m3u has been moved'
    else:
        print 'There was no merged.m3u file in place.'

    f = open(FIRSTFILE, 'r')
    text = f.read()
    f.close()
    with open(out, "a") as myfile:
        myfile.write(text)

    downrest = []
    downrest = os.listdir(DOWNLOADRESTFOLDER)
    total = len(downrest)
    if total > 0:
        for k in downrest:
            m3ufile = os.path.join(DOWNLOADRESTFOLDER, k)
            f = open(m3ufile, 'r')
            text = f.read()
            f.close()
            with open(out, "a") as myfile:
                myfile.write(text.replace('#EXTM3U#','').replace('#EXTM3U',''))
				
    appendrest = []
    appendrest = os.listdir(APPENDFOLDER)
    total = len(appendrest)
    if total > 0:
        for k in appendrest:
            m3ufile = os.path.join(APPENDFOLDER, k)
            f = open(m3ufile, 'r')
            text = f.read()
            f.close()
            with open(out, "a") as myfile:
                myfile.write(text.replace('#EXTM3U#','').replace('#EXTM3U',''))				
				
				
				
    xbmc.executebuiltin('Notification(m3us have been, merged)')

printstar()
print ('DOWNLOADFIRSTFOLDER is %s'% DOWNLOADFIRSTFOLDER)
# print ('testfile is %s'% testfile)
print ('OLDFILE is %s'% OLDFILE)
if os.path.exists(OLDFILE):
    os.remove(OLDFILE)

if os.path.isfile(FIRSTFILE):
    os.rename(FIRSTFILE, OLDFILE)
    print 'check 1'
else:
    print 'check 2'

IPTVFILE.retrieve("http://stream.fabiptv.com:25461/get.php?username=oqrfxtzg&password=m7q38iA3wE&type=m3u_plus&output=mpegts", FIRSTFILE)
xbmc.sleep(1000)
print 'check 3'
if os.path.exists(FIRSTFILE):
    xbmc.executebuiltin('Notification(Way, hey)')
else:
    xbmc.executebuiltin('Notification(Boo, hoo)')

mergefiles()
	








