# -*- coding: utf-8 -*-
# generic starting functions

# import
import xbmc
import xbmcgui
import os
import time
from time import gmtime, strftime

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def getdateandtime():
    global dateandtime
    dateandtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

# Run this first, so can define in terms of thisaddon:
def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
    getdateandtime()
    printstar()
    print ('%s has started'% thisaddon)
    print ('dateandtime is %s'% dateandtime)        # gives time in GMT
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

# run startaddon() to generate thisaddon, so can continue
startaddon()

# sources required for MARKER
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "test.txt")




# default messages
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
error3 = 'none'
error4 = 'none'
errornotification = 'none'
errordialogheader = 'none'
message = 'none'       # set default to 'none'; only print if changed

# errors
def errormessage():
    global error, error2, errornotification
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    try:
        if not error == 'none':
            print error
    except:
        pass
    try:
        if not error2 == 'none':
            print error2
    except:
        pass
    try:
        if not error3 == 'none':
            print error3
    except:
        pass
    try:
        if not error3 == 'none':
            print error3
    except:
        pass
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
    timemin = xbmc.getInfoLabel('System.Time(mm)')
    timemin = int(timemin) * 60
    timesec = xbmc.getInfoLabel('System.Time(ss)')
    timesec = int(timesec)
    timenow = timemin + timesec
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

def gettimediff():
    global timediff
    timefile = open(MARKER, 'r')
    filetime = timefile.read()
    timefile.close()
    print ('filetime is %s'% filetime)
    filetime = int(filetime)
    timediff = timenow - filetime
    print ('timediff is %d'% timediff)

def checkmarkerloop():
    c = 0
    while c < 1000000:
        if os.path.isfile(MARKER):
            xbmc.sleep(1000)
            visible = xbmcgui.getCurrentWindowDialogId()
            print ('visible is %d'% visible)
            if not visible == 12002:
                c = c + 1
            else:
                c = 1000000
                xbmc.sleep(10000)
#                xbmc.executebuiltin( "XBMC.Action(Select)" )
                xbmc.executebuiltin('SendClick(11)')
                xbmc.executebuiltin('Notification(Luvverly, jubberly)')
        else:
            xbmc.sleep(1000)
            c = c + 1

# continue startup
# check MARKER stuff
# get system time
checktime()
# check if marker present - if so stop script, if not make it
# checkmarkeratstart()

# check if marker present.  If present run checktime
# if timediff < 1hr loop; if > 1hr close running script
checkmarkerloop()
exit()
