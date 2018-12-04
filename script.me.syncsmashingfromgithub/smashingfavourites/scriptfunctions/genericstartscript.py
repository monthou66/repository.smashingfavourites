# -*- coding: utf-8 -*-
# generic starting functions

# import
import xbmc
import xbmcgui
import os
import sys
import shutil
from time import gmtime, strftime

# sources
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
LOGFOLDER = os.path.join(SMASHINGFAVOURITES, "logfiles")
smashinglog = os.path.join(LOGFOLDER, "smashinglog.log")
smashingoldlog = os.path.join(LOGFOLDER, "smashingoldlog.log")

# defaults
startedfromscript = 'false'
choice = 'false'
force = 'false'
logmessage = 'none'
logmessage2 = 'none'
logmessage3 = 'none'
logmessage4 = 'none'
logmessage5 = 'none'
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
error3 = 'none'
error4 = 'none'
errornotification = 'none'
errordialogheader = 'none'
message = 'none'       # set default to 'none'; only print if changed


#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def getdateandtime():
    global dateandtime
    print 'running getdateandtime()'
    dateandtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
def processtime():
    print 'running getdateandtime()'
    # example dateandtime: 2017-08-05 18:17:06
#    seconds = dateandtime[-2:]
    seconds = int(dateandtime[17:19])
    minutes = int(dateandtime[14:16])
    hours = int(dateandtime[11:13])
    day = int(dateandtime[8:10])
    month = int(dateandtime[5:7])
    year = int(dateandtime[:4])
    print ('year is %s'% year)
    print ('month is %s'% month)
    print ('day is %s'% day)
    print ('hour is %s'% hours)
    print ('minutes are %s'% minutes)
    print ('seconds are %s'% seconds)
#    exit()

def printlog():
    global logmessage, logmessage2, logmessage3, logmessage4, logmessage5
    print 'running printlog()'
    getdateandtime()
    starter = ('\n%s %s'%(dateandtime, thisaddon))
    starter = (starter+"                                        ")[:55] # this adds 40 spaces to starter but cuts the max length to 55 characters
    message = ('%s %s'%(starter, logmessage))
    with open(smashinglog, "a") as myfile:
        myfile.write(message)
    if not logmessage2 == 'none':
        message = ('%s %s'%(starter, logmessage2))    
        with open(smashinglog, "a") as myfile:
            myfile.write(message)
        logmessage2 = 'none'
        if not logmessage3 == 'none':
            message = ('%s %s'%(starter, logmessage3))    
            with open(smashinglog, "a") as myfile:
                myfile.write(message)
            logmessage3 = 'none'
            if not logmessage4 == 'none':
                message = ('%s %s'%(starter, logmessage4))    
                with open(smashinglog, "a") as myfile:
                    myfile.write(message)
                logmessage4 = 'none'
                if not logmessage5 == 'none':
                    message = ('%s %s'%(starter, logmessage5))    
                    with open(smashinglog, "a") as myfile:
                        myfile.write(message)
                    logmessage5 = 'none'

def checklogsize():
    print 'running checklogsize()'
    size = os.path.getsize(smashinglog)
    if size > 500000:
        # delete smashingoldlog, rename, make new log
        if os.path.isfile(smashingoldlog):
            os.remove(smashingoldlog)
            xbmc.sleep(300)
        os.rename(smashinglog, smashingoldlog)
        newsmashinglog()
        
def newsmashinglog():
    global thisaddon, logmessage
    print 'running newsmashinglog()'
    open(smashinglog, "w").close()
    thisaddon = "                "
    logmessage = 'smashinglog.log\n'
    printlog()
    # remove first (blank) line from logfile
    with open(smashinglog, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(smashinglog, 'w') as fout:
        fout.writelines(data[1:])
    
# Run this first, so can define in terms of thisaddon:
def startaddon():
    global thisaddon, logmessage
    print 'running startaddon()'
    # check log exists
    if os.path.isfile(smashinglog):
        checklogsize()
    else:
        newsmashinglog()
    thisaddon = sys.argv[0]
    printstar()
    logmessage = '%s has started'% thisaddon
    print logmessage
    printlog()
# run startaddon() to generate thisaddon, so can continue
startaddon()
# define MARKER
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "%sisrunning.txt"% thisaddon)

# errors
def errormessage():
    global error, error2, errornotification, logmessage, logmessage2, logmessage3, logmessage4, logmessage5
    print 'running errormessage()'
    printstar()
    logmessage = ('%s has stopped with an error'% thisaddon)
    print logmessage
    try:
        if not error == 'none':
            logmessage2 = error
            print error
    except:
        pass
    try:
        if not error2 == 'none':
            logmessage3 = error2
            print error2
    except:
        pass
    try:
        if not error3 == 'none':
            logmessage4 = error3
            print error3
    except:
        pass
    try:
        if not error3 == 'none':
            logmessage5 = error4
            print error3
    except:
        pass
    printlog()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    # try marker stuff - delete it if present, otherwise it will stop the script running next time
    if os.path.exists(MARKER):
        print ('MARKER exists at %s'% MARKER)
        try:
            os.remove(MARKER)
            if not os.path.exists(MARKER):
                print 'MARKER has been removed'
                xbmc.sleep(300)
        except:
            print ('The marker file (%s) could not be deleted'% MARKER)
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(Marker file - was not removed)')
    else:
        print ('No MARKER file to delete at %s'% MARKER)
    try:
        if not errornotification == 'none':
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(errornotification)')
    except:
        pass
    try:
        if not errordialogheader == 'none':
            xbmc.sleep(3000)
            xbmcgui.Dialog().ok(errordialogheader, *errordialoglist)    # need * to use with list or errors out
    except:
        pass
    printstar()
    exit()    
    
def checktime():
    global timenow
    print 'running checktime()'
    timehr = xbmc.getInfoLabel('System.Time(hh)')
    timehrsecs = int(timehr) * 3600
    timemin = xbmc.getInfoLabel('System.Time(mm)')
    timeminsecs = int(timemin) * 60
    timesec = xbmc.getInfoLabel('System.Time(ss)')
    timesec = int(timesec)
    timenow = timehrsecs + timeminsecs + timesec
    print ('timenow is %d'% timenow)

def checkmarkeratstart():
    global error, error2, error3, errordialogheader, errordialoglist
    print 'running checkmarker()'
    if os.path.isfile(MARKER):
        timefile = open(MARKER, 'r')
        filetime = timefile.read()
        timefile.close()
        print ('filetime is %s'% filetime)
        filetime = int(filetime)
        timediff = timenow - filetime
        # in case go over date
        if filetime > timenow:
            timediff = 86400 + timenow - filetime
            print 'timediff adjusted because crossed to new day'
        print ('timediff is %d'% timediff)
        # if script shut down correctly MARKER file won't exist.
        # if it does generate an error message, remove MARKER and exit the script
        error = 'Problem found running checkmarkeratstart()'
        error2 = ('A MARKER file was found at %s'% MARKER)
        error3 = ('The MARKER file was produced %d seconds before this script was started'% timediff)
        errordialogheader = 'Script stopped'
        errordialoglist = []
        line1 = 'marker file problem - checkmarkerstart() function'
        line2 = ('of %s failed because'% thisaddon)
        line3 = 'there was a marker already there'
        line4 = MARKER
        errordialoglist.append(line1)
        errordialoglist.append(line2)
        errordialoglist.append(line3)
#        errordialoglist.append(line4)      # only works with max 3 variables
        errormessage()
    else:
        print ('No MARKER file found at %s'% MARKER)
        print 'MARKER file will be made now'
        marker = open(MARKER, 'w')
        marker.write("%d" % timenow)
        marker.close()

             
      
processtime()    

    
    
    
# continue startup
# check MARKER stuff
# get system time
checktime()
# check if marker present - if so stop script, if not make it
checkmarkeratstart()
