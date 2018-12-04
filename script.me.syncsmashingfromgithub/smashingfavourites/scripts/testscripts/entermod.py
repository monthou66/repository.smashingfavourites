# -*- coding: utf-8 -*-

import os
import xbmc
import sys

# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
markersfolder = os.path.join(SMASHINGTEMP, "markers")
timestamp = os.path.join(markersfolder, "timestampletters.txt")


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def checkfolders():
    global error, error2
    print 'running checkfolders()'
    # check folder structure is in place - make if necessary
    foldersmade = []
    folderstocheck = []
    folderstocheck.append(SMASHINGTEMP)
    folderstocheck.append(markersfolder)
    num = len(folderstocheck)
    c = 0
    while c < num:
        check = folderstocheck[c]
        if not os.path.isdir(check):
            os.mkdir(check)
            xbmc.sleep(300)
            if not os.path.isdir(check):
                print 'Problem in checkfolders()'
                print ('Could not make %s folder'% check)
                xbmc.executebuiltin('Notification(Problem, check log)')
                exit()
            foldersmade.append(check)
        c = c + 1
    size = len(foldersmade)
    if size > 0:
        print ('New folders made: %d'% size)
        e = 0
        while e < size:
            next = foldersmade[e]
            print next
            e = e + 1
    
def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    if not os.path.isdir(markersfolder):
        checkfolders()
    
def checktime():
    timemin = xbmc.getInfoLabel('System.Time(mm)')
    timemin = int(timemin) * 60
    timesec = xbmc.getInfoLabel('System.Time(ss)')
    timesec = int(timesec)
    timenow = timemin + timesec   
    timefile = open(timestamp, 'r')
    filetime = timefile.read()
    filetime = int(filetime)    
    timediff = timenow - filetime
    if timediff >= 5:
#        os.remove(timestamp)
        xbmc.executebuiltin( "Select" )
        print 'check1'
        exit()
    print 'check2'
    exit()

startaddon()    
if os.path.isfile(timestamp):
    checktime()
else:
    xbmc.executebuiltin( "Select" )
    print 'check3'
    exit()