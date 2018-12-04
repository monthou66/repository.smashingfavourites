# -*- coding: utf-8 -*-

import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')

LOGPATH = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(LOGPATH, "kodi.log")
OLDLOGFILE = os.path.join(LOGPATH, "kodi.old.log")
#printstar()
#print ('logfile is %s' % LOGFILE)
#printstar()

GROUPS = []


printstar()
with open(OLDLOGFILE) as f:
    for line in f:
        if "DEBUG: PVR - Get - group" in line:
            start = "group '"
            end = "' loaded from the database"
            grp = (line.split(start))[1].split(end)[0]
            print grp
            GROUPS.append(grp)
        if "TV groups fetched from the database" in line:
             print line
			 
# lose duplicates and 'RADIO'
TVGROUPS = []			 
for i in GROUPS:			 
    if i not in TVGROUPS:
        if not i == 'Radio':
            TVGROUPS.append(i)

tvnum = len(TVGROUPS)		 
print 'GROUPS are:'
print TVGROUPS
print ('There are %d tv groups' % tvnum)
printstar()
# print list line-by-line:
c = 0
while c < tvnum:
    print TVGROUPS[c]
    c = c + 1
print 'And that\'s yer lot'

