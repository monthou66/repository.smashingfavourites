# -*- coding: utf-8 -*-

import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
thisaddon = sys.argv[0]
printstar()
print ('%s has started'% thisaddon)
xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

LOGPATH = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(LOGPATH, "kodi.log")
OLDLOGFILE = os.path.join(LOGPATH, "kodi.old.log")
#printstar()
#print ('logfile is %s' % LOGFILE)
#printstar()

	
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

xbmc.sleep(3000)
print 'radio channel groups loaded'

finishline = 'not found'
with open(LOGFILE) as f:
    lines = f.readlines()
    w = 1
    while w < 100:
        finishline = lines[-w]
        if 'radio channel groups loaded' in finishline:
            printstar()
            print ('finishline is %s'% finishline)
            printstar()
            w = w + 100
        w = w + 1
if finishline == 'not found':
    printstar()
    print ('finishline not found.  %s will close now.'% thisaddon)
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
xbmc.executebuiltin('Notification(%s, all done)'% thisaddon)



