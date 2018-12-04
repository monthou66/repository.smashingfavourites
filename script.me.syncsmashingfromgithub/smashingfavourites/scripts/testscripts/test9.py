# -*- coding: utf-8 -*-
# get masterprofile
import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

USERDATA = xbmc.translatePath('special://masterprofile')
MSTERPRO = USERDATA[:8]
if MSTERPRO == 'C:\Users':
    build = 'boring'
else:
    build = 'portable'

	
printstar()
print "test9.py has just been started"
print ('build is %s' % build)
print ('USERDATA = %s' % USERDATA)
print ('MSTERPRO = %s' % MSTERPRO)
#print ('testy = %s' % testy)
printstar()
xbmc.executebuiltin('Notification(test4.py, started)')