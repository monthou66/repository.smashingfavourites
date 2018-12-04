# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import os

USERDATA = xbmc.translatePath('special://masterprofile')
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
# hackyhacks
restartheader = 'wibble'

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def toggledebug():
    # read debug line in log, change as required
    # restart kodi
    global restartheader
    if debugsetting == 'enable':
        delete_start = ["loglevel>0<"]
        replacestart = "loglevel>1<"
        expected = '<loglevel>0</loglevel>'
        unexpected = '<loglevel>1</loglevel>'
    elif debugsetting == 'disable':
        delete_start = ["loglevel>1<"]
        replacestart = "loglevel>0<"
        expected = '<loglevel>1</loglevel>'
        unexpected = '<loglevel>0</loglevel>'		
    else:
        print 'problem detected - no valid debugsetting found.'
        exit()	    
    if os.path.exists(ADVANCEDSETTINGS) and os.path.isfile(ADVANCEDSETTINGS):
        lines = file(ADVANCEDSETTINGS, 'r').readlines()
        debugcurrent = lines[-11].strip()
        if debugcurrent == expected:
            # edit file
            infile = ADVANCEDSETTINGS
            outfile = os.path.join(USERDATA, "advancedsettingstemp.xml")
#            delete_start = ["loglevel>0<"]
            delete_end = ["/loglevel"]
            fin = open(infile)
            fout = open(outfile, "w+")
            for line in fin:
                for word in delete_start:
                    line = line.replace(word, replacestart)
                for word in delete_end:
                    line = line.replace(word, "/loglevel")	
                fout.write(line)
            fin.close()
            fout.close()
            os.remove(infile)
            os.rename(outfile, infile)
            restartheader = ('Debug logging has been %sd in advanced settings' % debugsetting)
            restart()
        elif debugcurrent == unexpected:
            restartheader = ('Debug logging was already %sd in advanced settings' % debugsetting)
            restart()			
        else:
            print 'No log settings found.'
            print ('debugcurrent = %s' % debugcurrent)
    else:
        print 'No advanced settings found.'

def restart():
    yesnowindow = xbmcgui.Dialog().yesno(restartheader,"Click yes to re-start now and apply new settings","Click No or exit to do apply on next re-start")






debugsetting = 'enable'
toggledebug()	
printstar()
print "test5.py has just been started"
print 'done it by George'
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')