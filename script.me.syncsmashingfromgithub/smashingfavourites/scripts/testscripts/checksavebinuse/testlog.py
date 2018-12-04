# -*- coding: utf-8 -*-

import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

FOLDER = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(FOLDER, "kodi.log")
#hackyhacks
result = 'no idea'

def testlog():
    global test
    global loglevel
    global result
    if os.path.exists(LOGFILE) and os.path.isfile(LOGFILE):
        c = 0
        d = -1
        lines = file(LOGFILE, 'r').readlines()
        while c < 10:
            test = lines[d].rstrip()
            loglevel = test[test.find("T")+6:test.find(": ")]
            loglevel = loglevel.strip()
            if loglevel == 'DEBUG':
                result = 'woohoo'
                c = c + 1
            else:
                result = 'boohoo'
                c = c + 1
            d = d - 5
            print result
    else:
        test = 'ohnoes'

testlog()	
printstar()
print ("LOGFILE returns as %s" % LOGFILE)
print ("test returns as %s" % test)
print ("loglevel returns as %s" % loglevel)
print result
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')
exit()

	
	
	