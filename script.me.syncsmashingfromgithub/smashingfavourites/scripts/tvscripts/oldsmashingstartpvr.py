#!/usr/bin/python
# -*- coding: utf-8 -*-
# startpvr.py

######################################################################################################################################################
######################################################################################################################################################
##  Start / stop pvr and change addon data from shortcut or dialog
##  Options
##  -------
##  'pvraddon = xxx' 
##  'pvraddon = choose' - choose pvr group
##  'pvraddon = current' - keep same; if multiple ignore singular flag; assume data is unchanged
##  'disable' - disable all pvr addons, temp = true
##  'cleardb' disable, refresh, swap db for empty one
##  'reset' - cleardb + temp = true + multiple = false
##  'permanent' = enable marker addon; stops automatic disabling by service addon
##  'multiple' - enable multiple simultaneous pvr's
##  'singular' - only 1 enabled
##  'temp' = disable marker addon (default!)
##  'group = xxx' / 'group = all' / 'group = choose'
##  'choose' - choose pvraddon; reset; default data (so use 'choose, data = choose' to choose both)
##  'data = xxx' / 'data = current' / data = 'previous' / 'data = default' / 'data = choose' > new data to move in      
##  force = just do it, no prompts
##  quiet = no notifications
##  channels            - jump to
##  guide               - jump to
##  radio               - jump to
##  recordings          - jump to
##  timers              - jump to
##  search              - jump to
##  recordedfiles       - jump to
##  timeshift           - jump to
##  
##  
######################################################################################################################################################
######################################################################################################################################################

import xbmc
import xbmcgui
import os
import os.path
import sys
import shutil
import json
from time import gmtime, strftime

# define some places
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))
LOGPATH = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(LOGPATH, "kodi.log")
# ENABLE = os.path.join(ADDONSFOLDER, "script.me.pvrpermanentenable")
USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
MULTI = os.path.join(ADDONSFOLDER, "script.me.pvrmultienable")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONDATA = os.path.join(MISC, "addon_data")
SMASHINGADDONDATAOPTIONS = os.path.join(MISC, "addon_data.options")
markersfolder = os.path.join(SMASHINGTEMP, "markers")
PERMANENT = os.path.join(markersfolder, "pvr.permanentenable.txt")
SMASHINGLOGFOLDER = os.path.join(SMASHINGTEMP, "logfiles")
smashinglog = os.path.join(SMASHINGLOGFOLDER, "smashinglog.log")
smashingoldlog = os.path.join(SMASHINGLOGFOLDER, "smashingoldlog.log")
EMPTYDBFOLDER = os.path.join(MISC, "emptypvrdatabase")


# defaults
pvraddon = 'not set'
force = 'false'
quiet = 'false'
default = 'false'
window = 'channels'
channels = 'not set'        # not set defaults to true
guide = 'false'
permanent = 'not set'     # can be true, false, all, name of addon (in which case it's additive)
temp = 'not set'           # set as false if permanent = true 
multiple = 'not set'
data = 'current'
disable = 'false'
refreshdb = 'false'
cleardb = 'false'
group = 'none'
version = 'unknown'
disabled = 'false'
refreshed = 'false'
dbcleared = 'false'
reset = 'false'
previousdata = 'false'
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
endmessage = 'All, done'        # default notification for finish()

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"
    
def getdateandtime():
    global dateandtime
    print 'running getdateandtime()'
    dateandtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

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

# errors
def errormessage():
    global error, error2, error3, error4, errornotification, logmessage, logmessage2, logmessage3, logmessage4, logmessage5
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
                    
def error():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Check, %s)'% thisaddon)
    exit()

def checkfolders():
    global error, error2
    print 'running checkfolders()'
    # check folder structure is in place - make if necessary
    foldersmade = []
    folderstocheck = []
    folderstocheck.append(SMASHINGTEMP)
    folderstocheck.append(SMASHINGLOGFOLDER)
    folderstocheck.append(markersfolder)
    num = len(folderstocheck)
    c = 0
    while c < num:
        check = folderstocheck[c]
        if not os.path.isdir(check):
            os.mkdir(check)
            xbmc.sleep(300)
            if not os.path.isdir(check):
                error = 'Problem in checkfolders()'
                error2 = ('Could not make %s folder'% check)
                errormessage()
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
    global thisaddon, version, NEWTVDB, error, error2
    thisaddon = sys.argv[0]
    checkfolders()
    # get kodi version:
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    # response is eg >> json_query is {"id":1,"jsonrpc":"2.0","result":{"name":"Kodi","version":{"major":17,"minor":4,"revision":"20170717-b22184d","tag":"releasecandidate","tagversion":"1"}}}
    start = 'major":'
    finish = ',"minor'
    version = (json_query.split(start))[1].split(finish)[0]
    version = int(version)
    if version == 17:
        OLDTVDB = os.path.join(USERDATA, "Database", "TV29.db")
        NEWTVDB = os.path.join(EMPTYDBFOLDER, "TV29.db")
    elif version == 18:
        OLDTVDB = os.path.join(USERDATA, "Database", "TV31.db")
        NEWTVDB = os.path.join(EMPTYDBFOLDER, "TV31.db")
    elif version == 16:
        OLDTVDB = os.path.join(USERDATA, "Database", "TV29.db")
        NEWTVDB = os.path.join(EMPTYDBFOLDER, "TV29.db")
    else:
        error = 'Problem in startaddon()'
        error2 = ('NEWTVDB not identified because no setting for version %d.'% version)
        errormessage()
    printstar()
    print ('%s has started'% thisaddon)
    print ('kodi version is %d'% version)
    printstar()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
	
def checkpvrnotplaying():
    if (xbmc.getCondVisibility("Player.Playing")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')
        exit()
    elif (xbmc.getCondVisibility("Player.HasMedia")):
        xbmc.executebuiltin('Notification(Close player, before making changes)')
        exit()
    elif (xbmc.getCondVisibility("Pvr.IsPlayingTv")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()
    elif (xbmc.getCondVisibility("Pvr.IsPlayingRadio")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()
    elif (xbmc.getCondVisibility("Pvr.IsPlayingRecording")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()

def gohome():
    global error
    # check if in home window
    window = xbmcgui.getCurrentWindowId()
    if not window == 10000:
        # add 'back' because Home doesn't work if in groups dialog
        xbmc.executebuiltin( "XBMC.Action(Back)" )
        xbmc.executebuiltin("ActivateWindow(Home)")
        xbmc.sleep(300)
        window = xbmcgui.getCurrentWindowId()        
        if not window == 10000:
            error = 'Problem in gohome()'
            errormessage()
        
def getarguments():
    global pvraddon, window, channels, guide, disable, refresh, cleardb, reset, permanent, temp, group, data, force, quiet, error, error2
    print 'running getarguments()'
    number = len(sys.argv)
    c = 1
    while c < number:
        arg = sys.argv[c]
        if arg[:11] == 'pvraddon = ':
            pvraddon = arg[11:0]        # ie argument is 'pvraddon = xyz', addon (script variable) is 'xyz'
            if pvraddon == 'choose':
                choosepvr = 'true'
            elif pvraddon == 'current':
                currentpvr = 'true'
        elif arg[:4] == 'pvr.':
            pvraddon = arg
            if pvraddon == 'choose':
                choosepvr = 'true'
            elif pvraddon == 'current':
                currentpvr = 'true'
        elif arg == 'channels':
            window = 'channels'
            channels = 'true'
            if number == 2:
                quiet = 'true'
                simpletvchannels()
        elif arg == 'guide':
            window = 'guide'
            guide = 'true'
            channels = 'false'
            if number == 2:
                quiet = 'true'
                simpletvguide()
        elif arg == 'radio':
            window = 'radio'
            if number == 2:
                quiet = 'true'
                radio()
                finish()
        elif arg == 'recordings':
            window = 'recordings'
            if number == 2:
                quiet = 'true'
                recordings()
                finish()
        elif arg == 'timers':
            window = 'timers'
            if number == 2:
                quiet = 'true'
                timers()
                finish()        
        elif arg == 'search':
            window = 'search'
            if number == 2:
                quiet = 'true'
                search()
                finish()        
        elif arg == 'recordedfiles':
            window = 'recordedfiles'
            if number == 2:
                quiet = 'true'
                recordedfiles()
                finish()    
        elif arg == 'timeshift':
            window = 'timeshift'
            if number == 2:
                quiet = 'true'
                timeshift()
                finish()      
        elif arg == 'choose':
            pvraddon = 'choose'
            choosepvr = 'true'
            data = 'current'
            refreshdb = 'true'
            cleardb = 'true'
            reset = 'true'
            temp = 'true'
            permanent = 'false'
            multiple = 'false'
        elif arg == 'disable':
            disable = 'true'
            refreshdb = 'true'
            cleardb = 'true'
            temp = 'true'
            permanent = 'false'
        elif arg == 'refresh':
            refreshdb = 'true'
        elif arg == 'cleardb':
            refreshdb = 'true'
            cleardb = 'true'
        elif arg == 'reset':
            refreshdb = 'true'
            cleardb = 'true'
            temp = 'true'
            permanent = 'false'
            multiple = 'false'
        elif arg == 'temp':
            temp = 'true'
            permanent = 'false'
        elif arg == 'permanent':
            permanent = 'true'
            temp = 'false'
        elif arg == 'multiple':
            multiple = 'true'
        elif arg == 'singular':
            multiple = 'false'
        elif arg[:8] == 'group = ':
            group = arg[8:]
        elif arg[:7] == 'data = ':
            data = arg[7:]
            if data == 'choose':
                choosedata = 'true'
        elif arg == 'default':
            data = 'default'
        elif arg == 'force':
            force = 'true'
        elif arg == 'quiet':
            quiet = 'true'
#        elif arg == radio:
        else:
            error = 'Problem in getarguments()'
            error2 = ('Invalid argument can not be processed: %s'% arg)
            errormessage()
        c = c + 1            
            
def getpvrs():
    global disabled, pvrs, pvrnumber, activepvrs, activepvrnumber, error
    print 'running getpvrs()'
    # get list of potentially active pvr's - ones that have folders in addon_data
    check = []
    pvrs = []
    activepvrs = []
    if not xbmc.getCondVisibility('System.HasPVRAddon'):
        disabled = 'true'
        print 'check disabled'
    else:
        print 'check not disabled'
    check = os.listdir(ADDONDATA)
    print ('check = %s'% check)
    num = len(check)
    print ('num = %d'% num)
    c = 0
    while c < num:
        next = check[c]
        print ('next = %s'% next)
        if next[:4] == 'pvr.':
            if 'previous' not in next:
                pvrs.append(next)
                print ('next(%s) was appended to pvrs list'% next)
                if xbmc.getCondVisibility('System.HasAddon(%s)'% next):
                    print ('next(%s) was appended to activepvrs list'% next)
                    activepvrs.append(next)
                else:
                    print ('next(%s) is not enabled, so not appended to activepvrs list'% next)
            else:
                print ('next(%s) was not appended to pvrs list'% next)


        c = c + 1
    pvrnumber = len(pvrs)
    activepvrnumber = len(activepvrs)
    print ('pvrs list is %s'% pvrs)
    print ('activepvrs list is %s'% activepvrs)
    print ('pvrnumber is %d'% pvrnumber)
    print ('activepvrnumber is %d'% activepvrnumber)
    if pvrnumber == 0:
        error = 'No potentially active pvr addons found - none have folders in addon_data.'
        errormessage()
        
        
def oldgetarguments():
    # get arguments - to find which pvr addon to start - and which group?  Incorporate in SmashingTV
    global pvraddon, number, a, b, c
    pvraddon = sys.argv[1]			# which pvr addon - 'disable' = turn all off
                                    # if starts with 'refresh' clear database then load named addon - eg 'refreshpvr.dvbviewer
                                    # if pvraddon = 'refresh' just clear the database
                                    # if pvraddon = 'cleardb' disable, refresh, swap db for empty one
									# 'permanent' = enable marker addon
									# 'temp' = disable marker addon
    number = len(sys.argv)
    print ('number is %d'% number)

    if len(sys.argv) > 2:
        a = sys.argv[2]     # channels or guides etc
    else:
        a = 'channels'
    if a == 0:
        a = 'channels'	
		
    if len(sys.argv) > 3:
        b = sys.argv[3]		# which group
        c = 2				# use to count to right group
    else:
        b = 0
        g = 1				# All channels opened by default
        g = int(g)
			
def checkwantedsettings():
    global pvraddon, disabled, refreshed, dbcleared, dataoptionsfolder, defaultfile, addondatasub, previousdatasub, tempdatasub
    print 'running checkwantedsettings()'
    # checking
    print ('pvraddon is %s'% pvraddon)
    if disable == 'true':
        if not disabled == 'true':
            # check if in home window
#            window = xbmcgui.getCurrentWindowId()
#            if not window == 10000:
                # add 'back' because Home doesn't work if in groups dialog
#                xbmc.executebuiltin( "XBMC.Action(Back)" )
#                xbmc.executebuiltin("ActivateWindow(Home)")
            stoppvr()
    print ('refreshdb is %s'% refreshdb)
    if refreshdb == 'true':
        print 'refreshdb = true'
        refresh()
    else:
        print 'refreshdb != true'
    if cleardb == 'true':
        if not disabled == 'true':
            stoppvr()
        if not refreshed == 'true':
            refresh()
        replacedatabase()
    if reset == 'true':
        if not disabled == 'true':
            stoppvr()
        if not refreshed == 'true':
            refresh()
        if not dbcleared == 'true':
            replacedatabase()
        permanentdisable()
        multidisable()        
    if permanent == 'true':
        permanentenable()
    if permanent == 'false':
        permanentdisable()
    if multiple == 'true':
        multienable()
    if multiple == 'false':
        multidisable()
    if pvraddon == 'none':
        finish()
    if pvraddon == 'choose':
        choosepvr()
#    if pvraddon == 'current':
#        if xbmc.getCondVisibility('System.HasPVRAddon'):
#        # data stays unchanged, check channels / groups / group = and go
#            setf()                                                            # change name!
#        else:
#            if activepvrnumber == 0:
#                error = 'No pvr addon was active so could not set pvr == current'
#                errormessage()
#            elif activepvrnumber == 1:
#                pvraddon = activepvrs[0]
#                                            # start single pvr
#            else:
#                pvraddons = []
#                pvraddons = activepvrs
#                                                # start multiple pvrs
    elif pvraddon == 'current':
        if not xbmc.getCondVisibility('System.HasPVRAddon'):
            error = 'No pvr addon was active so could not set pvr == current'
            errormessage()
    elif pvraddon == 'not set':
        pass
    else:
        # process pvraddon
        if not xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
            if not multiple == 'true':
                if not disabled == 'true':
                    stoppvr()
                    if not refreshed == 'true':
                        refresh()
                        replacedatabase()
            # start that sucker
            print 'start that sucker'
            startpvr()
            wait()
    if not group == 'none':
        getchannelgroups()
                
                
    
    
    
    
    # At this point we must know what pvraddon is, so can set more variables:
    dataoptionsfolder = os.path.join(SMASHINGADDONDATAOPTIONS, pvraddon)
    defaultfile = os.path.join(dataoptionsfolder, "default.txt")
    addondatasub = os.path.join(ADDONDATA, pvraddon)
    oldaddon = pvraddon + '.previous settings'
    previousdatasub = os.path.join(ADDONDATA, oldaddon)
    tempaddon = pvraddon + '.temp'
    tempdatasub = os.path.join(ADDONDATA, tempaddon)    
    processdatafiles() 
    print ('data = %s'% data)
    if data == 'choose':
        getdata()
    elif not data == 'current':
        checkdata()
        
        
def choosepvr():
    global pvraddon, error, error2
    print 'running choosepvr()'
    # list possibles from addondata, smashingaddondata, smashingaddondataoptions
    check = []
    pvrchoice = []
    check = os.listdir(ADDONDATA)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            pvrchoice.append(next)
        c = c + 1
    check = []
    check = os.listdir(SMASHINGADDONDATA)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if next not in pvrchoice:
                pvrchoice.append(next)
        c = c + 1
    check = []
    check = os.listdir(SMASHINGADDONDATAOPTIONS)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if next not in pvrchoice:
                pvrchoice.append(next)
        c = c + 1
    num = len(pvrchoice)
    if num == 0:
        add = 'There are no valid pvr addons to choose from'
        pvrchoice.append(add)
    cancel = 'Cancel operation'
    pvrchoice.append(cancel)
    # Choose
    CHOOSE = xbmcgui.Dialog().select("Choose pvr addon", pvrchoice)
    CHOICE = pvrchoice[CHOOSE]
    if CHOOSE == -1:
        error = 'Problem in choosepvr()'    
        error2 = 'Script cancelled by user'
        errormessage()
    elif CHOICE == add:
        error = 'Problem in choosepvr()'    
        error2 = 'Script cancelled by user'
        errormessage()
    elif CHOICE == cancel:
        error = 'Problem in choosepvr()'    
        error2 = 'Script cancelled by user'
        errormessage()
    else:
        pvraddon = CHOICE
    
def processdatafiles():
    global currentversion, previousversion, defaultversion
    print 'running processdatafiles()'
    # set defaults
    currentversion = 'none'
    previousversion = 'none'
    defaultversion = 'none'    
    currentversionfile = os.path.join(addondatasub, "version.txt")
    previousversionfile = os.path.join(previousdatasub, "version.txt")    
    if os.path.exists(currentversionfile):
        f = open(currentversionfile, "r")
        currentversion = f.read()    
    print ('currentversion is %s'% currentversion)                  # currentversion is 'none' if not read here   
    if os.path.exists(previousversionfile):
        f = open(previousversionfile, "r")
        previousversion = f.read()
    print ('previousversion is %s'% previousversion)                  # previousversion is 'none' if not read here
    if os.path.exists(defaultfile):
        f = open(defaultfile, "r")
        defaultversion = f.read()    
    print ('defaultversion is %s'% defaultversion)          # defaultversion is 'none' if not read here    
    
def getdata():
    global pvraddon, data, previousdatasub, previousdata, backup, error, error2, currentversion, previousversion, defaultversion
    print 'running getdata()'
    # list current state before proceeding: ie currentversion, previousversion, defaultversion
    dialoglist = []
    a = ('Current version is %s'% currentversion)
    b = ('Previous version is %s'% previousversion)
    c = ('Default version is %s'% defaultversion)
    dialoglist.append(a)
    dialoglist.append(b)
    dialoglist.append(c)
    xbmcgui.Dialog().ok(pvraddon, *dialoglist)    # need * to use with list or errors out
   
    previous = 'false'
    removebackup = 'false'
    # list alternatives (if any)
#    dataoptionsfolder = os.path.join(SMASHINGADDONDATAOPTIONS, addon)
    # check folder exists - if not create it:
    if not os.path.isdir(dataoptionsfolder):
        os.mkdir(dataoptionsfolder)
    # list subfolders - exclude any files
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
    if os.path.isdir(previousdatasub):
        previous = 'Load previous addon data'
        dataoptions.append(previous)
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
    elif CHOICE == previous:
        previousdata = 'true'
        data = 'previous'
        print ('data is %s'% data)
        switchtopreviousdata()
    else:
        data = CHOICE
        print ('data is %s'% data)
        switchdata()

def checkdata():
    global data, error, error2, previousdatasub
    print 'running checkdata()'
    # check specified data subfolder exists
    trypath = os.path.join(SMASHINGADDONDATAOPTIONS, pvraddon, data)
    if previousdata == 'true':
        if os.path.isdir(previousdatasub):
            print 'checkdata() passed'
            switchtopreviousdata() 
        else:
            xbmc.executebuiltin('Notification(Script cancelled, previous addon data not found)')
            error = 'Problem in checkdata'
            error2 = ('previousdatasub (%s) does not exist'% previousdatasub)
            errormessage()    
    elif os.path.isdir(trypath):
        print 'checkdata() passed'
        print ('data is %s'% data)
        switchdata()
    else:
        xbmc.executebuiltin('Notification(Script cancelled, addon_data folder not found)')
        error = 'Problem in checkdata'
        error2 = ('data subfolder (%s) does not exist'% trypath)
        errormessage()
    
def switchtopreviousdata():
#    global 
    print 'running switchtopreviousdata()'
    # check if addon is running
#    disableaddon()    
    # do the switcheroo    
    shutil.move(previousdatasub, tempdatasub)
    shutil.move(addondatasub, previousdatasub)
    xbmc.sleep(300)
    shutil.move(tempdatasub, addondatasub)
    # (re)enable addon
#    enableaddon()    
    
def switchdata():
    global data
    print 'running switchdata()'
    # check if addon is running
#    disableaddon()
    # do the switcheroo
    newdatasub = os.path.join(dataoptionsfolder, data)
    if not os.path.isdir(tempdatasub):
        os.mkdir(tempdatasub)
    if os.path.isdir(previousdatasub):
        shutil.move(previousdatasub, tempdatasub)
    shutil.move(addondatasub, previousdatasub)
    xbmc.sleep(300)
    shutil.copytree(newdatasub, addondatasub)
    xbmc.sleep(300)
    shutil.rmtree(tempdatasub)
    # (re)enable addon
#    enableaddon()





def replacedatabase():
    global error
    # delete the old database
    c = 0
    while c < 50:
        try:
            os.remove(OLDTVDB)
            xbmc.sleep(300)
        except:
            pass
        if not os.path.isfile(OLDTVDB):    
            c = 1000
        else:
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(TV database, refreshing)')
            xbmc.sleep(1000)
            c = c + 1
    if c < 1000:
        error = ('Could not delete OLDTVDB(%s)'% OLDTVDB)
        errormessage()
    # and move in a new empty one
    c = 0
    while c < 50:
        try:
            shutil.copyfile(NEWTVDB, OLDTVDB)
            xbmc.sleep(300)
        except:
            pass
        if os.path.isfile(OLDTVDB):
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(TV database, refreshed)')
            c = 1000
        else:
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(TV database, refreshing)')
            xbmc.sleep(1000)
            c = c + 1
    if c < 1000:
        error = ('Could not copy NEWTVDB (%s) into the Database folder'% NEWTVDB)
        errormessage()

def checkcurrentpvr():
    global STOP
    # check if the addon is already running - if not continue startup
	# check if any pvr running - if so stop.
    # then start pvraddon
    if not xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            stoppvr()
            xbmc.executebuiltin('Notification(Stopping, %s)'% STOP)
            refresh()

#            exit()
            checkready()
        startpvr()
        xbmc.executebuiltin('Notification(Starting, %s)'% pvraddon)
#        exit()		
        checkstarted()
		
def setf():
    global a, f
    if a in ["Channels", "channels", "Channel", "channel"]:
        f = 1
        f = int(f)
    elif a in ['Guide', 'guide']:
        f = 2
        f = int(f)
    elif a in ['Radio', 'radio']:
        radio()
    elif a in ['Recordings', 'recordings', 'Recorded', 'recorded', 'Recorded TV', 'recorded tv']:
        recordings()	
    elif a in ['Timers', 'timers']:
        timers()
    elif a in ['Search', 'search']:
        search()	
    elif a in ['Recorded files', 'Recorded Files', 'recorded files', 'recordedfiles', 'Files', 'files']:
        recordedfiles()	
    elif a in ['Timeshift', 'timeshift']:
        timeshift()
    else:
        f = 1
        f = int(f)
        printstar()
        print ('Problem with sys.argv1 in smashingtv. Script read a as %s but set f to 1' % a)
        printstar() 

def getchannelgroups():
    global CHANNELGROUPS, channelgroups, numbergroups
    CHANNELGROUPS = []
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
    channelgroups = ret['result']['channelgroups']
    for channelgroup in channelgroups:
#        printstar()
#        print channelgroup
        chanstring = str(channelgroup)
        start = "u'label': u'"
        end = "'}"		
        group = (chanstring.split(start))[1].split(end)[0]
        CHANNELGROUPS.append(group)
#    print CHANNELGROUPS
    numbergroups = len(CHANNELGROUPS)
    print ('There are %d channel groups' % numbergroups)
    c = 0
    while c < numbergroups:
        print CHANNELGROUPS[c]
        c = c + 1

def setchannelgroup():
    global group, groupnumber, numbergroups, CHANNELGROUPS, error        
    print 'running setchannelgroup()'    
    print ('There are %d channel groups'% numbergroups)
    print ('Channel groups are: %s'% CHANNELGROUPS)
    print ('The wanted group is %s'% group)
    c = 0
    groupnumber = 0             # defaults to 'choose'
    while c < numbergroups:
        GRP = CHANNELGROUPS[c]
        if group == GRP:
            groupnumber = c + 1
        c = c + 1
    if group in ["Choose", "choose", "Choose Group", "choose group"]:
        groupnumber = 0
    print ('Channel group number set to %d'% groupnumber)
    
        
def setg():
    global b, g, CHANNELGROUPS, channelgroups, numbergroups
    c = 0
    g = 0
    print 'Now starting setg()'
    print CHANNELGROUPS
    print ('numbergroups is %s'% numbergroups)
    print ('b is %s'% b)
    while c < numbergroups:
        GRP = CHANNELGROUPS[c]
        print ('CHANNELGROUPS[%d] is %s'% (c, GRP))
        if b == CHANNELGROUPS[c]:		
# try c + 1 ??????????
            g = c + 1
        c = c + 1
    if b in ["Choose", "choose", "Choose Group", "choose group"]:	
        g = 0
        print ('b read as %s' % b)
        print 'g set as 0 - choose group'
    print ('g is %s'% g)
    print ('The channel group is %s'% b)
    
# open channel or guide windows	- f = 1,2
def opengroups():
    global groupnumber
    if guide == 'true': 
	    xbmc.executebuiltin('ActivateWindow(TVGuide)')	
    else:
	    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    xbmc.executebuiltin('SendClick(28)')
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
    # loop move down to correct group (if necessary)
    c = 1
    if groupnumber > 1:
	    while (c < groupnumber):	
		    c = c + 1
		    xbmc.executebuiltin( "XBMC.Action(Down)" )			
    # open group if not using 'choose' option.		
    if groupnumber >= 1:		
	    xbmc.executebuiltin( "XBMC.Action(Select)" )
	    xbmc.executebuiltin( "XBMC.Action(Right)" )
	    xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )

    
# Check if PERMANENT file (smashing/miscfiles/markers/pvr.permanentenable.txt) exists.  If not make it.
def permanentenable():
    global error
    print 'running permanentenable()'
    if not os.path.isfile(PERMANENT):
        open(PERMANENT,"w").close()
        xbmc.sleep(300)
    if os.path.isfile(PERMANENT):
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Permanent, marker set)')
    else:
        error = ('PERMANENT marker(%s) not created'% PERMANENT)
        errormessage()
        
        
def permanentdisable():
    print 'running permanentdisable()'
    if os.path.isfile(PERMANENT):
        os.remove(PERMANENT)
        xbmc.sleep(300)
    if not os.path.isfile(PERMANENT):
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Permanent, marker removed)')
    else:
        error = ('PERMANENT marker(%s) not removed'% PERMANENT)
        errormessage()

# Check if MULTI file (smashing/miscfiles/markers/pvr.multienable.txt) exists.  If not make it.
def multienable():
    global error
    print 'running multienable()'
    if not os.path.isfile(MULTI):
        open(MULTI,"w").close()
        xbmc.sleep(300)
    if os.path.isfile(MULTI):
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Multiple pvr, marker set)')
    else:
        error = ('MULTI marker(%s) not created'% MULTI)
        errormessage()
        
        
def multidisable():
    print 'running multidisable()'
    if os.path.isfile(MULTI):
        os.remove(MULTI)
        xbmc.sleep(300)
    if not os.path.isfile(MULTI):
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Multiple pvr, marker removed)')
    else:
        error = ('MULTI marker(%s) not removed'% MULTI)
        errormessage()
		
def radio():
    print 'running radio()'
    xbmc.executebuiltin('ActivateWindow(radiochannels)')
    finish()	

# f=4
def recordings():
    xbmc.executebuiltin('ActivateWindow(tvrecordings)')
    finish()

# f=5	
def timers():
    xbmc.executebuiltin('ActivateWindow(tvtimers)')
    finish()

# f=6	
def search():
    xbmc.executebuiltin('ActivateWindow(tvsearch)')
    finish()
	
# pvr can be disabled for recorded files - f=7
def recordedfiles():
    xbmc.executebuiltin('Videos,smb://SourceTVRecordings/,return')
    finish()
	
# pvr can be disabled for timeshift files - f=8
def timeshift():
    xbmc.executebuiltin('Videos,smb://SourceTVTimeshift/,return')   # opens the timeshift folder directly
    finish()
    
def simpletvchannels():
    xbmc.executebuiltin('ActivateWindow(TVChannels)')       # opens pvr://channels/tv/All channels/
    finish()
    
def simpletvguide():
    xbmc.executebuiltin('ActivateWindow(TVGuide)')
    finish()

	
def stoppvr():
    global ADDONSFOLDER, STOP, pvrs, pvrnumber, disabled, quiet, error, error2
    print 'running stoppvr()'
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        # check for pvr's that have folders in addon_data:
#        print ('%s check 11'% thisaddon)
        c = 0
        while c < pvrnumber:
            checkpvr = pvrs[c]
            print ('checking for %s'% checkpvr)
            if xbmc.getCondVisibility('System.HasAddon(%s)'% checkpvr):
                checkreadytostop()
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% checkpvr)            
                xbmc.sleep(1000)
            c = c + 1
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            error = 'Problem in stoppvr()'
            error2 = 'Not all pvrs were disabled.'
            errormessage()
        else:
            print 'All pvr addons disabled'
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(Live TV, has been disabled)')                
            disabled = 'true'
    else:
        print 'No pvr addons were enabled'
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Live TV, was not enabled)')
        disabled = 'true'


def oldstoppvr():
    global ADDONSFOLDER, STOP
    print 'running stoppvr()'
    # quick check - is pvr active? are dvbviewer / iptvsimple active?  Then check the rest.
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        # add 'back' because Home doesn't work if in groups dialog
        xbmc.executebuiltin( "XBMC.Action(Back)" )
        xbmc.executebuiltin("ActivateWindow(Home)")
        xbmc.sleep(300)
        print ('%s check 11'% thisaddon)	
        if xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):
            checkreadytostop()
            print ('%s check 12'% thisaddon)
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')            
#			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')
            STOP = 'dvbviewer'
        if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
            print ('%s check 13'% thisaddon)
            checkreadytostop()
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')
#            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')
            STOP = 'iptvsimple'
	# check if any other pvr addons are installed.  If yes stop them
    print ('%s check 14'% thisaddon)
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        PATHADDONS = [d for d in os.listdir(ADDONSFOLDER) if os.path.isdir(os.path.join(ADDONSFOLDER, d))]
        ALTADDONS = [d for d in os.listdir(DEFAULTADDONSFOLDER) if os.path.isdir(os.path.join(DEFAULTADDONSFOLDER, d))]
        ALLADDONS = PATHADDONS + ALTADDONS
        ALLPVR = [s for s in ALLADDONS if "pvr." in s]
        printstar()
        print ('ALLPVR is %s'% ALLPVR)	
        printstar()		
        x = len(ALLPVR)
        y = 0
        while y < x:
            CHECK = ALLPVR[y]
            if xbmc.getCondVisibility('System.HasAddon(%s)'% CHECK):
                checkreadytostop()
                print ('disabling %s'% CHECK)
                STOP = CHECK
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s","enabled":false}}'% CHECK)
                xbmc.sleep(1000)
                printstar()
                print 'check 1'
                if not xbmc.getCondVisibility('System.HasPVRAddon'):
                    y = x
                    printstar()
                    print 'check 2'				
#                    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% pvraddon)
            y = y + 1				
    printstar()
    print ('%s check 15'% thisaddon)
    # and a bit more
    refresh()
    xbmc.executebuiltin('Notification(PVR disabled, database refreshed)')
# next copy default db

def wait():
    print 'running wait()'
    # check the pvr info box isn't showing - if it is, wait!
    if xbmc.getCondVisibility('System.HasPVRAddon'):
#        xbmc.executebuiltin("ActivateWindow(Home)")   
        v = 0
        while v < 120:                                                              # ie 2 minutes
            pvrloading = xbmc.getCondVisibility('Window.IsVisible(10151)')          # extendeddialoginfo
            if pvrloading == 0:                                                     # ie dialog not visible
                xbmc.executebuiltin('Notification(Please, wait)')
                xbmc.sleep(5000)                                                    # wait 5 sec
                pvrloadingcheck = xbmc.getCondVisibility('Window.IsVisible(10151)')
                if pvrloadingcheck == 0:                                            # and check again
                    v = 1000
                else:
                    xbmc.executebuiltin('Notification(Please, wait)')
                    v = v + 1
            else:
                xbmc.sleep(1000)
                xbmc.executebuiltin('Notification(Please, wait)')
                v = v + 1
        if v < 1000:
            xbmc.executebuiltin('Notification(Timed out, please try again)')
            exit()

def checkreadytostop():
    print 'running checkreadytostop()'
    # check the pvr info box isn't showing - if it is, wait!
    if xbmc.getCondVisibility('System.HasPVRAddon'):
#        xbmc.executebuiltin("ActivateWindow(Home)")   
        v = 0
        while v < 120:                                                              # ie 2 minutes
            pvrloading = xbmc.getCondVisibility('Window.IsVisible(10151)')          # extendeddialoginfo
            if pvrloading == 0:                                                     # ie dialog not visible
                xbmc.executebuiltin('Notification(Stopping, now)')
                xbmc.sleep(5000)                                                    # wait 5 sec
                pvrloadingcheck = xbmc.getCondVisibility('Window.IsVisible(10151)')
                if pvrloadingcheck == 0:                                            # and check again
                    v = 1000
                else:
                    xbmc.executebuiltin('Notification(False alarm, waiting to stop safely)')
                    v = v + 1
            else:
                xbmc.sleep(1000)
                xbmc.executebuiltin('Notification(Hang on a tick, waiting to stop safely)')
                v = v + 1
        if v < 1000:
            xbmc.executebuiltin('Notification(Not safe to stop pvr, try again)')
            exit()

def refresh():
    global refreshed
    print 'running refresh()'
# refresh the pvr database	
    xbmc.executebuiltin("ActivateWindow(10021)")
#    xbmc.executebuiltin("UnloadSkin()")
    xbmc.executebuiltin("SetFocus(-70)")
    xbmc.executebuiltin( "XBMC.Action(Select)" )
#    exit()
    xbmc.executebuiltin('SendClick(11)')
#    xbmc.executebuiltin("ActivateWindow(Home)")
#    xbmc.executebuiltin("ReloadSkin()")
    refreshed = 'true'
    if not quiet == 'true':
        xbmc.executebuiltin('Notification(Live TV, has been refreshed)')
            
def oldrefresh():
    global refreshed
    print 'running stoppvr()'
# refresh the pvr database	
    xbmc.executebuiltin("ActivateWindow(10021)")
    xbmc.executebuiltin("UnloadSkin()")
    xbmc.executebuiltin("SetFocus(-70)")
    xbmc.executebuiltin( "XBMC.Action(Select)" )
    xbmc.executebuiltin('SendClick(11)')
    xbmc.executebuiltin("ActivateWindow(Home)")
    xbmc.executebuiltin("ReloadSkin()")
    refreshed = 'true'
    if not quiet == 'true':
        xbmc.executebuiltin('Notification(Live TV, has been refreshed)')	

def startpvr():	
    global pvraddon	
    print ('%s is not running'% pvraddon)
    # check system has the addon in the argument - otherwise generate a notification
    PATH = os.path.join(ADDONSFOLDER, pvraddon)
    ALTPATH = os.path.join(DEFAULTADDONSFOLDER, pvraddon)
    print ('PATH is %s'% PATH)
    print ('ALTPATH is %s'% ALTPATH)
    if not os.path.exists(PATH):
        if os.path.exists(ALTPATH):
            PATH = ALTPATH
        else:
            printstar()
            print ('Tried to start %s but the addon is not installed.'% pvraddon)
            printstar()
            xbmc.executebuiltin('Notification(%s, is not installed)'% pvraddon)
            error()
            exit()
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% pvraddon)
    printstar()
    print 'check 4'	
	
# try again
def try2checkready():	
    global LOGFILE, starttime, length, startlog	
    found = 'false'
    h = 1
    w = startlog
    while h <= 49:
        with open(LOGFILE) as f:
            lines = f.readlines()            
            finishline = lines[w]
            if 'radio channel groups loaded' in finishline:
                finishlog = w + 1
                h = 50
                print ('finishline is %s'% finishlog)
                xbmc.sleep(300)
                xbmc.executebuiltin('Notification(finishline is line, %s)'% finishlog)
            w = w + 1
        xbmc.sleep(1000)
        h = h + 1
    if not h == 51:
        printstar()
        print ('finishline not found.  %s will close now.'% thisaddon)
        error()
        exit()
    else:
        xbmc.executebuiltin('Notification(finishline is line, %s)'% finishlog)

# and again
def checkready():	
    global STOP	
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    checkcount = 0
    while checkcount < 30:
        if not xbmc.getCondVisibility('System.HasAddon(%s)'% STOP):
            if not xbmc.getCondVisibility('Pvr.HasTVChannels'):
                checkcount = 30
                xbmc.sleep(1000)
        checkcount = checkcount + 1
    if checkcount == 30:
#        xbmc.executebuiltin('Notification(Oh, poop)')
        exit()

def checkstarted():
    global pvraddon
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    checkcount = 0
    while checkcount < 30:
        if xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
            if xbmc.getCondVisibility('Pvr.HasTVChannels'):
                checkcount = 30
                xbmc.sleep(1000)
        checkcount = checkcount + 1
        xbmc.sleep(300)
    if checkcount == 30:
#        xbmc.executebuiltin('Notification(Oh, poop)')
        exit()
	
# lose this
def realcheckready():
    # check the log for 'radio channel groups loaded' after the script started - if that appears it's safe to switch to a pvr window
    global LOGFILE, starttime
    found = 'false'
    h = 1
    while h <= 49:
        with open(LOGFILE) as f:
            lines = f.readlines()
            w = 1
            while w < 500:
                finishline = lines[-w]
                if ('%s has started'% thisaddon) in finishline:
                    xbmc.sleep(300)
                    w = 500				
                elif 'radio channel groups loaded' in finishline:
                    printstar()
                    print ('finishline is %s'% finishline)
                    printstar()
                    found = 'true'
                    w = 500
                w = w + 1
#                print ('w is %s'% w)
        if found == 'false':
            h = h + 1
            printstar()
#            print ('h is %s'% h)
        else:
            h = 50
#            h = h + 20
            printstar()
            print ('h is %s'% h)
    if found == 'false':
        printstar()
        print ('finishline not found. %s will stop'% thisaddon)
        printstar()		
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
    if starttime > finishtime:
        printstar()
        print ('starttime > finishtime: %s will exit'% thisaddon)		
        printstar()
    xbmc.sleep(300)
#    xbmc.executebuiltin('ActivateWindow(TVChannels)')
#    exit()	

def finish():
    global endmessage
    print 'running finish()'
    print ('%s stopping'% thisaddon)
    # notifications:
    if not quiet == 'true':
        if not endmessage == 'none':
            xbmc.executebuiltin('Notification(endmessage)')
    exit()
		
      
# Get on with it.
# print 'check 1'
startaddon()
# print ('%s check 2'% thisaddon)
checkpvrnotplaying()
# print ('%s check 3'% thisaddon)
# checkstart()


getarguments()
# print ('%s check 4'% thisaddon)
gohome()

getpvrs()   # list what's potentially running now, to check

checkwantedsettings()
# print ('%s check 5'% thisaddon)
checkcurrentpvr()
# print ('%s check 6'% thisaddon)
# follow it through gets to end of startpvr() if required - chosen pvr is running, now look at window.
# checkready()



getchannelgroups()

setchannelgroup()

opengroups()

exit()


	
