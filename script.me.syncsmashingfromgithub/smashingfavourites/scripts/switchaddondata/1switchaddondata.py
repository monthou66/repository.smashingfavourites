# -*- coding: utf-8 -*-

######################################################################################################################################################
######################################################################################################################################################
##  change addon data from shortcut or dialog
##  Options
##  -------
##  addon = addon (foldername) to change     format 'addon = ...'
##  backup = backup existing data first
##  nobackup = delete existing data
##  data = new data to move in      format 'data = ...'
##  force = just do it, no prompts
##  default = load default data
## 
######################################################################################################################################################
######################################################################################################################################################

import xbmc
import xbmcgui
import os
import shutil
from time import gmtime, strftime

print 'starting switchaddondata.py'

# sources
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))        # this is the read-only default folder
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))   
USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONDATA = os.path.join(MISC, "addon_data")
LOGFOLDER = os.path.join(SMASHINGTEMP, "logfiles")
smashinglog = os.path.join(LOGFOLDER, "smashinglog.log")
smashingoldlog = os.path.join(LOGFOLDER, "smashingoldlog.log")
# path to working advancedsettings.xml
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")




# defaults
addon = 'none'
# backup = 'true'
nobackup = 'false'
force = 'false'
default = 'false'
data = 'none'
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





#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
    
def getdateandtime():
    global dateandtime
    print 'running getdateandtime()'
    dateandtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

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
        
        
# Run this first, so can define in terms of thisaddon:
def startaddon():
    global thisaddon, logmessage
    print 'running startaddon()'
    # check log exists
    if not os.path.isfile(smashinglog):
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
    
def getoptions():
    global error, error2, addon, data, backup, nobackup
    print 'running getoptions()'
    size = len(sys.argv)
    print ('size is %s'% size)
    if len(sys.argv) > 1:
        c = 1
        num = len(sys.argv)
        while c < num:
            d = sys.argv[c]
            if d[:5] == 'addon':
                addon = d[8:]
                print ('addon is %s'% addon)
            elif d[:4] == 'data':
                data = d[7:]
                print ('data is %s'% data)
            elif d == 'backup':
                backup = 'true'
                nobackup = 'false'
            elif d == 'nobackup':
                nobackup = 'true'
                backup = 'false'
            else:
                error = 'Invalid argument'
                error2 = ('Argument (%s) not recognised'% d)
                errormessage()
            c = c + 1

def getaddon():
    global addon, error, error2, logmessage
    print 'running getaddon()'
    # list options - check SMASHINGADDONDATA folder for subfolders containing DEFAULT + >=1; then check if addon is present.
    options = []        # list all folders in SMASHINGADDONDATA with an alternative
    checkaddondata = os.listdir(SMASHINGADDONDATA)
    num = len(checkaddondata)
    c = 0
    while c < num:
        checkfolder = checkaddondata[c]
        checkfolderpath = os.path.join(SMASHINGADDONDATA, checkfolder)
        checkdefaultpath = os.path.join(checkfolderpath, "default")
        if os.path.isdir(checkdefaultpath):
            subfolders = os.listdir(checkfolderpath)
            size = len(subfolders)
            if size > 1:
                d = 0
                while d < size:
                    sub = subfolders[d]
                    checksubfolder = os.path.join(checkfolderpath, sub)
                    if os.path.isdir(checksubfolder):
                        if not checksubfolder == 'default':
                            options.append(checkfolder)
                            d = size
                    d = d + 1
        c = c + 1
    # check addons in OPTIONS list are installed
    if len(options) == 0:
        logmessage = 'No available options to choose from.'
        printlog()
        xbmc.executebuiltin('Notification(No options, available)')
        exit()
    e = 0
    f = len(options)
    while e < f:
        g = options[e]
        trypath = os.path.join(ADDONSFOLDER, g)
        if not os.path.isdir(trypath):
            trypath = os.path.join(DEFAULTADDONSFOLDER, g)
            if not os.path.isdir(trypath):
                options.remove(g)
        e = e + 1
    if len(options) == 0:
        logmessage = 'No available options to choose from.'
        printlog()
        xbmc.executebuiltin('Notification(No options, available)')
        exit()
    # choose addon from options list
    cancel = 'Cancel script'
    options.append(cancel)
    CHOOSE = xbmcgui.Dialog().select("Choose addon", options)
    CHOICE = options[CHOOSE]
    if CHOICE == cancel:
        error = 'Stopped in getaddon()'
        error2 = 'Script cancelled by user'
        errormessage()
    elif CHOOSE == -1:
        error = 'Stopped in getaddon()'
        error2 = 'No valid choice made by user'
        errormessage()
    else:
        addon = CHOICE
        print ('addon is %s'% addon)

def checkaddon():
    global addon, error, error2
    print 'running checkaddon()'
    # check addon folder exists
    trypath = os.path.join(ADDONSFOLDER, addon)
    if not os.path.isdir(trypath):
        trypath = os.path.join(DEFAULTADDONSFOLDER, addon)
        if not os.path.isdir(trypath):
            error = 'Problem in checkaddon'
            error2 = ('Addon folder (%s) does not exist'% addon)
            errormessage()
    print 'checkaddon() passed'
    print ('addon is %s'% addon)

        
def getdata():
    global addon, data, error, error2
    print 'running getdata()'
    # list alternatives (if any)
    dataoptionsfolder = os.path.join(SMASHINGADDONDATA, addon)
    # check default folder exists:
    defaultfolder = os.path.join(dataoptionsfolder, "default")
    if not os.path.isdir(defaultfolder):
        error = 'Problem in getdata()'
        error2 = ('No default folder in %s'% dataoptionsfolder)
        errormessage()
    # list subfolders
    datafoldercontents = []
    dataoptions = []
    datafoldercontents = os.listdir(dataoptionsfolder)
    num = len(datafoldercontents)
    c = 0
    while c < num:
        check = datafoldercontents[c]
        trypath = os.path.join(dataoptionsfolder, check)
        if os.path.isdir(trypath):
            dataoptions.append(check)
        c = c + 1
    # add extra choices
    cancel = 'Cancel script'
    dataoptions.append(cancel)
    CHOOSE = xbmcgui.Dialog().select("Choose addon data", dataoptions)
    CHOICE = dataoptions[CHOOSE]
    if CHOICE == cancel:
        error = 'Stopped in getdata()'
        error2 = 'Script cancelled by user'
        errormessage()
    elif CHOOSE == -1:
        error = 'Stopped in getdata()'
        error2 = 'No valid choice made by user'
        errormessage()
    else:
        data = CHOICE
        print ('data is %s'% data)

def checkdata():
    global data, error, error2
    print 'running checkdata()'
    # check specified data subfolder exists
    trypath = os.path.join(SMASHINGADDONDATA, addon, data)
    if not os.path.isdir(trypath):
        error = 'Problem in checkdata'
        error2 = ('data subfolder (%s) does not exist'% trypath)
        errormessage()
    print 'checkdata() passed'
    print ('data is %s'% data)
    
def processbackup():
    global error, error2, logmessage
    print 'running processbackup()'
    backupfile = os.path.join(ADDONDATA, addon, "version.txt")
    defaultfile = os.path.join(ADDONDATA, addon, "default.txt")
    if os.path.exists(backupfile):
        f = open(backupfile, "r")
        oldversion = f.read()
        logmessage = ('oldversion is %s'% oldversion)
        print ('oldversion is %s'% oldversion)
        printlog()
    if os.path.exists(defaultfile):
        f = open(defaultfile, "r")
        defaultversion = f.read()
        logmessage = ('defaultversion is %s'% defaultversion)
        print ('defaultversion is %s'% defaultversion)
        printlog()    
    


def finish():
    print 'running finish()'
    if os.path.isfile(MARKER):
        os.remove(MARKER)
    xbmc.executebuiltin('Notification(Scrip completed, all done)')
    exit()

    
    
checktime()
# check if marker present - if so stop script, if not make it
checkmarkeratstart()
    
getoptions()
if addon == 'none':
    getaddon()
else:
    checkaddon()
if data == 'none':
    getdata()
else:
    checkdata()
if not nobackup == 'true':
    processbackup()
finish()