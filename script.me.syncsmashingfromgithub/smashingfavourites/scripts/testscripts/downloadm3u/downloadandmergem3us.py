# -*- coding: utf-8 -*-
# downloadandmergem3us.py
import xbmc
import urllib
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "downloadandmergem3us.py has started"
printstar()
# xbmc.executebuiltin('Notification(downloadandmergem3us.py, started)')


# checking age of last merged file.
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
IPTVFOLDER = os.path.join(SMASHINGTEMP, "iptv")
DOWNLOADFIRSTFOLDER = os.path.join(IPTVFOLDER, "downloadfirst")
FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, 'fabiptv.m3u')
TIMEFIRSTFILE = os.path.getmtime(FIRSTFILE)
TEMP = os.path.join(DOWNLOADFIRSTFOLDER, 'temp.txt')
TEMPFILE = open(TEMP, 'w')
TIMETEMPFILE = os.path.getmtime(TEMP)
AGEFIRST = TIMETEMPFILE - TIMEFIRSTFILE

print ('FIRSTFILE is %d seconds old'% AGEFIRST)
printstar()
exit()


# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
IPTVFOLDER = os.path.join(SMASHINGTEMP, "iptv")
SETTINGS = os.path.join(IPTVFOLDER, "settings.txt")
DOWNLOADFIRSTFOLDER = os.path.join(IPTVFOLDER, "downloadfirst")
# FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, 'fabiptv.m3u')
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
# Delete the merged.m3u from OLDFOLDER (oldout) and move merged.m3u from IPTVFOLDER in to replace it (out).
    if os.path.isfile(oldout):
        os.remove(oldout)	
    if os.path.isfile(out):
        os.rename(out, oldout)
        print 'merged.m3u has been moved'
    else:
        print 'There was no merged.m3u file in place.'
# read first downloaded .m3u into merged
    f = open(FIRSTFILE, 'r')
    text = f.read()
    f.close()
    with open(out, "a") as myfile:
        myfile.write(text)
# read any other downloaded .m3u files into merged
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
# read any local .m3u files into merged				
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

# Get on with it.
	
# empty OLDFOLDER
# Move files from DOWNLOADFIRSTFOLDER and DOWNLOADRESTFOLDER into OLDFOLDER

fileList = os.listdir(OLDFOLDER)
for fileName in fileList:
    print ('File to delete from old folder is %s'% fileName)
    DELETEME = os.path.join(OLDFOLDER, fileName)
    os.remove(DELETEME)

fileList = os.listdir(DOWNLOADFIRSTFOLDER)
for fileName in fileList:
    print ('File to move from downloadfirstfolder to old folder is %s'% fileName)
    MOVEME = os.path.join(DOWNLOADFIRSTFOLDER, fileName)
    MOVED = os.path.join(OLDFOLDER, fileName)
    os.rename(MOVEME, MOVED)		
		
fileList = os.listdir(DOWNLOADRESTFOLDER)
for fileName in fileList:
    print ('File to move from downloadrestfolder to old folder is %s'% fileName)
    MOVEME = os.path.join(DOWNLOADRESTFOLDER, fileName)
    MOVED = os.path.join(OLDFOLDER, fileName)
    os.rename(MOVEME, MOVED)

# Download m3us	
# read SETTINGS to get name and url for each .m3u file
# line 1 = name of FIRSTFILE, line 2 = url; line 3 = name of next download etc
if os.path.isfile(SETTINGS):
# count lines in file
    with open(SETTINGS) as foo:
        length = len(foo.readlines())
    links = length/2
    print ('length is %d lines'% length)
    print ('There are %d files to download'% links)
    lines = file(SETTINGS, 'r').readlines()
    FIRSTNAME = lines[0].rstrip()
    FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, FIRSTNAME)
    FIRSTLINK = lines[1].rstrip()
       		
    print ('FIRSTFILE is %s'% FIRSTFILE)
    print ('FIRSTLINK is %s'% FIRSTLINK)
    IPTVFILE.retrieve(FIRSTLINK, FIRSTFILE)	
    xbmc.sleep(1000)
# check if there are more links in SETTINGS
    if links > 1:
        p = 2
        while p < length:
            NEXTNAME = lines[p].rstrip()
            NEXTFILE = os.path.join(DOWNLOADRESTFOLDER, NEXTNAME)
            p = p + 1
            NEXTLINK = lines[1].rstrip()
            p = p + 1	
            IPTVFILE.retrieve(NEXTLINK, NEXTFILE)
            xbmc.sleep(1000)
else:		
    printstar()
    print "No valid settings file detected in iptvfolder"
    printstar()
    xbmc.executebuiltin('Notification(No valid settings file, in iptvfolder)')	
	
print 'check 3'
if os.path.exists(FIRSTFILE):
    xbmc.executebuiltin('Notification(Way, hey)')
else:
    xbmc.executebuiltin('Notification(Boo, hoo)')

mergefiles()
	








