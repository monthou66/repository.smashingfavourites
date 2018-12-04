# -*- coding: utf-8 -*-

import xbmc
import os

USERDATA = xbmc.translatePath('special://masterprofile')
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def enabledebug():
    # read debug line in log, change 0 to 1
    # restart kodi
    if os.path.exists(ADVANCEDSETTINGS) and os.path.isfile(ADVANCEDSETTINGS):
        lines = file(ADVANCEDSETTINGS, 'r').readlines()
        debugcurrent = lines[-11].strip()
        if debugcurrent == '<loglevel>0</loglevel>':
            # edit file
            infile = ADVANCEDSETTINGS
            outfile = os.path.join(USERDATA, "advancedsettingstemp.xml")
            delete_start = ["loglevel>0<"]
            delete_end = ["/loglevel"]
            fin = open(infile)
            fout = open(outfile, "w+")
            for line in fin:
                for word in delete_start:
                    line = line.replace(word, "loglevel>1<")
                for word in delete_end:
                    line = line.replace(word, "/loglevel")	
                fout.write(line)
            fin.close()
            fout.close()
            os.remove(infile)
            os.rename(outfile, infile)









enabledebug()	
printstar()
print "test5.py has just been started"
print 'done it by George'
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')