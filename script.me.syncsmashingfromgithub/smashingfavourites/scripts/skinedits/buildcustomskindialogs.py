# -*- coding: utf-8 -*-
# generic starting functions

# import
import xbmc
import xbmcgui
import os
import shutil
import sys
from time import gmtime, strftime

#hack!
sys.setrecursionlimit(10000)

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# sources
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))        # this is the read-only default folder
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))               # addons are normally installed in this folder
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
markersfolder = os.path.join(SMASHINGTEMP, "markers")
LOGFOLDER = os.path.join(SMASHINGTEMP, "logfiles")
smashinglog = os.path.join(LOGFOLDER, "smashinglog.log")
smashingoldlog = os.path.join(LOGFOLDER, "smashingoldlog.log")
BUILDFOLDER = os.path.join(SMASHINGTEMP, "buildcustomskindialogs")
mainoutputfolder = os.path.join(BUILDFOLDER, "output")
listfolder = os.path.join(BUILDFOLDER, "lists")
oldlistfolder = os.path.join(BUILDFOLDER, "lists.done")
workinglistfolder = os.path.join(BUILDFOLDER, "lists.working")
tempstart = os.path.join(workinglistfolder, "tempstart.xml")

favsfolder = os.path.join(SMASHINGFAVOURITES, "options")
optionsinfofolder = os.path.join(SMASHINGFAVOURITES, "optionsinfo")
activeskin = xbmc.translatePath('special://skin')
activeskin = activeskin[:-1]                    # removes backslash to match against skinfolder to check if need to reload skin

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
# more
favcount = 0
extraconditionsexist = 'false'
updateallskins = 'false'
updateskin = 'false'
addcustomdialogs = 'false'
newcustomdialogs = 'true'
reloadskin = 'false'

# get kodi version, check for matching folder in config, stop if not there
kodiversion = xbmc.getInfoLabel('System.BuildVersion')
kodiversion = kodiversion[:2]
printstar()
print 'Running buildcustomskindialogs.py'
print ('kodiversion is %s' % kodiversion)
printstar()

CONFIGALL = os.path.join(SMASHINGFAVOURITES, "scripts", "skinedits", "config")
CONFIG = os.path.join(CONFIGALL, kodiversion)

if not os.path.exists(CONFIG):
    error = ('No folder at %s' % CONFIG)
    errormessage()

blanksfolder = os.path.join(CONFIG, "blanks")  # contains subfolders for different versions
targetfolders = os.listdir(blanksfolder)



def checkfolders():
    global error, error2
    print 'running checkfolders()'
    # check folder structure is in place - make if necessary
    foldersmade = []
    folderstocheck = []
    folderstocheck.append(SMASHINGTEMP)
    folderstocheck.append(LOGFOLDER)
    folderstocheck.append(BUILDFOLDER)
    folderstocheck.append(mainoutputfolder)
    folderstocheck.append(listfolder)
    folderstocheck.append(oldlistfolder)
    folderstocheck.append(workinglistfolder)
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
    # check folder structure - make if necessary
    checkfolders()
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
MARKER = os.path.join(markersfolder, "%sisrunning.txt"% thisaddon)

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

def getoptions():
    global choice, force, startedfromscript, updateskin, updateallskins
    print 'running getoptions()'
    size = len(sys.argv)
    print ('size is %s'% size)
    if len(sys.argv) > 1:
        choice = 'true'
        c = 1
        num = len(sys.argv)
#        num = num + 1
        while c < num:
            d = sys.argv[c]
            if d == 'force':
                force = 'true'
            elif d == 'startedfromscript':
                startedfromscript = 'true'
            elif d == 'updateallskins':
                updateallskins = 'true'
            elif d[:11] == 'updateskin.':
                updateskin = d[6:]
            c = c + 1
    listfromfavs()
        
def getoptionssize():
#    global 
    print 'running getoptionssize()'
    sizefile = os.path.join(BUILDFOLDER, "favouritessize.txt")
    oldsize = 0
    if os.path.isfile(sizefile):
        with open(sizefile,'r') as f:
            oldsize = f.read()    
        print ('oldsize is %s bytes'% oldsize)
    favs = []
    favs = os.listdir(favsfolder)
    num = len(favs)
    c = 0
    totalsize = 0
    while c < num:
        d = favs[c]
        checkfile = os.path.join(favsfolder, d, "favourites.xml")
        if os.path.isfile(checkfile):
            size = os.path.getsize(checkfile)
            totalsize = totalsize + size
            c = c + 1
    print ('totalsize is %d bytes'% totalsize)
    if totalsize == 0:
        logmessage = 'Running getoptionsize(): no favourites found to process at %s'% favsfolder
        printlog()
        finish()
    # write to file and do stuff if it's changed
    totalsize = str(totalsize)
    if not totalsize == oldsize:
        text_file = open(sizefile, "w")
        text_file.write(totalsize)
        text_file.close()
    else:
        if not force == 'true':
            logmessage = 'Running getoptionsize(): favourites folder size has not changed(%s)'% favsfolder
            printlog()
            finish()    
    
def listfromfavs():
    # process existing favourites
    global favsfolder, listfolder, favsnumber, favslist
    print 'running listfromfavs()' 
    # check size of options folder
    getoptionssize()
    # list folders in favsfolder:
    favscontent = []
    favslist = []
    favscontent = os.listdir(favsfolder)
    favscontent.sort()                      # alphabetize
    num = len(favscontent)
    c = 0
    while c < num:
        test = favscontent[c]
        checkpath = os.path.join(favsfolder, test, "favourites.xml")
        if os.path.exists(checkpath):
            favslist.append(test)
        c = c + 1
    favsnumber = len(favslist)
    print ('favsnumber is %d'% favsnumber)   
    if favsnumber == 0:
        xbmc.executebuiltin('Notification(Stopping %s, No favourites to process)'% thisaddon) 
        logmessage = ('No favourites found in favsfolder (%s)'% favsfolder)
        printlog()
        finish()
#        xbmc.sleep(2000)
#        error()
    emptylistfolder()
    
def emptylistfolder():
    global DELETEFOLDER
    print 'emptylistfolder()'
    # check listfolder is empty 
    # checking
    print ('listfolder is %s'% listfolder)    
    if os.path.exists(listfolder):
        contents = os.listdir(listfolder)
        num = len(contents)
        if num > 0:
            DELETEFOLDER = listfolder
            # check
            print ('DELETEFOLDER is %s'% DELETEFOLDER)
            removefolder()
    if not os.path.exists(listfolder):
        os.mkdir(listfolder)
#    getfavs()
    emptyoutputfolders()
        
def getfavs():
    global favcount, NEWNAME, favourites, favouritesfile, ID, NEWLIST, NEWNAMEFULL
    print 'running getfavs()'
    if not favcount < favsnumber:
        print ('%d favourites files processed in getfavourites'% favcount)        
        # next step is to process lists
#        finish()
        listtasks()
    else:
        favourites = favslist[favcount]
        favouritesfile = os.path.join(favsfolder, favourites, "favourites.xml")    
        print ('favourites is %s'% favourites)
        print ('favouritesfile is %s'% favouritesfile)
        # get name from favourites file
        # Open favourites file, check last line for name and id.If present use those. 
        f = open(favouritesfile,"r")
        lines = f.readlines()
        lastline = lines[-1]
        print ('lastline is %s'% lastline)
        if lastline[:12] == '<!--name is ':
            start = '<!--name is '
            end = '-->'
            NEWNAME = (lastline.split(start))[1].split(end)[0]
            ID = NEWNAME[-4:]
            print ('NEWNAME is %s'% NEWNAME)
            print ('ID is %s'% ID)
            NEWNAMEFULL = NEWNAME + '.xml'
            NEWLIST = os.path.join(listfolder, NEWNAMEFULL)
            # check if file exists; if so delete it - no mercy.
            print ('NEWLIST is %s'% NEWLIST)
            if os.path.isfile(NEWLIST):
                os.remove(NEWLIST)
            if NEWNAME == 'Custom.smashing.alloptions2151':          # alloptions needs to be self-updating, so ignore the favourites.xml
                makealloptions()
            else:
                makenewlist()
        # else there isn't a name at the end of the favourites file - needs to be sorted before processing
        else:
            error = 'Problem with getfavs() function'
            error2 = 'The %s file doesn\'t have a properly formatted last line.'% favouritesfile
            error3 = 'Check this file before running the script again'
            errormessage()

def makenewlist():
    global favourites, NEWNAME, NEWLIST, ID, favcount, favouritesfile, str, line, extraconditionsexist
    print 'running makenewlist()'
    #open favourites file, read line 2 to get icon
    f = open(favouritesfile,"r")
    lines = f.readlines()
    line2 = lines[1]
    print ('line2 is %s'% line2)
    # check for presence of thumb - if not there generate error
    start = 'thumb="special://masterprofile/smashing/smashingfavourites/icons/'
    if start not in line2:
        error = 'Problem with makenewlist() function'
        error2 = 'The %s file doesn\'t have a valid icon in line 2.'% favouritesfile
        error3 = 'Check this file before running the script again'
        errormessage()        
    end = '.png"'
    icon = (line2.split(start))[1].split(end)[0]
    print ('icon is %s'% icon)
    #  print first 4 lines of newlist:
    line1 = ('<name>%s</name>\n'% NEWNAME)
    line2 = ('<id>%s</id>\n'% ID)
    line3 = ('<icon>%s</icon>\n'% icon)
    line4 = ('<list>			<!--  Dialog.Close(xxxx) if not specified; visible = true if not specified-->\n')
    with open(NEWLIST, "a") as myfile:
        myfile.write(line1)    
        myfile.write(line2)    
        myfile.write(line3)    
        myfile.write(line4)
# add first item - previous menu label:
        line5 = '<item>\n'
        line6 = '<label>Previous Menu</label>\n'
        line7 = '<onclick>RunScript(special://userdata/smashing/smashingfavourites/scripts/automatedscripts/opendialog.py, back)</onclick>\n'      
        line8 = '</item>\n'
    #with open(NEWLIST, "a") as myfile:
        myfile.write(line5)                     #   Adding first item (Previous Menu)
        myfile.write(line6)                     #   Same item on every file, but not in favourites ('cos not implemented)
        myfile.write(line7)                     #   Need to cancel the 'on-click close dialog' function later
        myfile.write(line8)                     #
# for each favourite pull out label and action    
#    favslength = len(lines) - 1
    favslength = len(lines) - 2         # -2 because added an extra 'name' line at the end of favourites - this needs looking at though     
    c = 1
    while c < favslength:
        line1 = '<item>\n'
        line = lines[c]
        start = '<favourite name="'
        stop = '"'
#        (firstline.split(start))[1].split(end)[0]
        line2build = (line.split(start))[1].split(stop)[0]
        line2 = ('<label>%s</label>\n'% line2build)        
        begin = '>'
        end = '<'
#        end = '</favourite>'  
#         line3 = (line.split(start))[1].split(end)[0] + '\n'       
        line3build = (line.split(begin))[1].split(end)[0]
# get rid of funny formatting    (eg amp)    
        str = line3build
        unescape()
# search for common favourites and specify onclick
# eg 'Choose More' > RunScript(special://masterprofile/smashing/smashingfavourites/scripts/smashingfavourites.py, choose)       
# becomes:
# 'Choose More' > ActivateWindow(2154,return)   ??? or  ActivateWindow(2154)
        if 'smashingletters.py,Next Letter' in str:
            str = str.replace('Next Letter', 'skinNext Letter')
        elif 'smashingletters.py,Previous Letter' in str:
            str = str.replace('Previous Letter', 'skinPrevious Letter')
        elif 'smashingfavourites.py' in str:
#        if 'RunScript(special://masterprofile/smashing/smashingfavourites/scripts/smashingfavourites.py' in str:
#        if str[:91] == 'RunScript(special://masterprofile/smashing/smashingfavourites/scripts/smashingfavourites.py':     
#        if str[:82] == 'RunScript(special://masterprofile/smashing/smashingfavourites/scripts/smashingfavourites.py': 
            scriptfavtoactwin()
        line3build = str        
        line3 = ('<onclick>%s</onclick>\n'% line3build)
        enditem = '</item>\n'
        checkformore = '<!--'
        if checkformore in line:
            extraconditionsexist = 'false'
            getextraconditions()
        with open(NEWLIST, "a") as myfile:
            myfile.write(line1)    
            myfile.write(line2)    
            myfile.write(line3)
            if extraconditionsexist == 'true':
                extraconditionsexist = 'false'          # reset or added to rest of list
                if not extracondition1 == 'false':
                    myfile.write(extracondition1)
                    if not extracondition2 == 'false':
                        myfile.write(extracondition2)
                        if not extracondition3 == 'false':
                            myfile.write(extracondition3)
                            if not extracondition4 == 'false':
                                myfile.write(extracondition4)
                                if not extracondition5 == 'false':
                                    myfile.write(extracondition5)
                                    if not extracondition6 == 'false':
                                        myfile.write(extracondition6)
            myfile.write(enditem)
        c = c + 1
    lastline = '</list>'
    with open(NEWLIST, "a") as myfile:
        myfile.write(lastline)
    favcount = favcount + 1
    getfavs()
    
def makealloptions():
    global favcount
    # favslist = all valid folders in favouritesfolder
    # remove alloptions (this!) and choose ('cos put at the top)
    print 'running makealloptions()'
    allfavs = []
    allfavs = favslist
#    if 'alloptions' in allfavs:
#        allfavs.remove('alloptions')
#        print 'alloptions removed from allfavs'
#    else:
#        error = 'Problem in makealloptions()'
#        error2 = 'Could not remove \'alloptions\' from allfavs'
#        error3 = 'allfavs is %s'% allfavs
#        errormessage()
#    if 'choose' in allfavs:
#        allfavs.remove('choose')
#        print 'choose removed from allfavs'
#    else:
#        error = 'Problem in makealloptions()'
#        error2 = 'Could not remove \'choose\' from allfavs'
#        error3 = 'allfavs is %s'% allfavs
#        errormessage()
    num = len(allfavs)
    # get start of list from blanksfolder
    startfileblank = os.path.join(blanksfolder, "Custom.smashing.alloptions2151.xml")
    alloptionsfile = os.path.join(listfolder, "Custom.smashing.alloptions2151.xml")
    shutil.copyfile(startfileblank, alloptionsfile)
    # for each folder in favslist open favourites.xml, get name, write (append) entry
    c = 0
    while c < num:
        subfolder = allfavs[c]
        ignorefile = os.path.join(favsfolder, subfolder, "ignorethisfolder.txt")
        print ('subfolder is %s'% subfolder)
        if subfolder == 'alloptions':
            print 'check alloptions'
        elif subfolder == 'choose':
            print 'check choose'
        elif os.path.exists(ignorefile):
            print ('The %s folder will not be added to alloptions'% subfolder)
        else:
            favsfile = os.path.join(favsfolder, subfolder, "favourites.xml")
            f = open(favsfile,"r")
            lines = f.readlines()
            lastline = lines[-1]
            if lastline[:12] == '<!--name is ':
                start = '<!--name is '
                end = '-->'
                smashingname = (lastline.split(start))[1].split(end)[0]
                smashingnumber = smashingname[-4:]
                start = '--><!--'
                end = '-->'
                menuname = (lastline.split(start))[1].split(end)[0]
                print ('smashingname is %s'% smashingname)
                print ('smashingnumber is %s'% smashingnumber)
                print ('menuname is %s'% menuname)
                line1 = '<item>\n'
                line2 = ('<label>%s</label>\n'% menuname)
                line3 = ('<onclick>RunScript(special://userdata/smashing/smashingfavourites/scripts/automatedscripts/opendialog.py, %s)</onclick>\n'% smashingnumber)
                line4 = '</item>\n'
                with open(alloptionsfile, "a") as myfile:
                    myfile.write(line1)    
                    myfile.write(line2)    
                    myfile.write(line3)    
                    myfile.write(line4)
        c = c + 1
    endline = '</list>'
    with open(alloptionsfile, "a") as myfile:
        myfile.write(endline)
    favcount = favcount + 1
    getfavs()
        
# get more conditions from end of line in favourites
def getextraconditions():
    global extraconditionsexist, extracondition1, extracondition2, extracondition3, extracondition4,extracondition5, extracondition6, line
    print 'Running getextraconditions()'
    extraconditionsexist = 'false'
    extracondition1 = 'false'
    extracondition2 = 'false'
    extracondition3 = 'false'
    extracondition4 = 'false'
    extracondition5 = 'false'
    extracondition6 = 'false'
    start = '</favourite>'
    # endofline = everything after </favourite>
    line = line.strip()
    endofline = line.split(start,1)[1]
    # checking
    print ('line is %s'% line)
    print ('endofline is %s'% endofline)
    # get rid of '<!--' - generate an error if '<!--' appears more than once
    num = len(endofline)
    checknum = num - 10
    c = 0
    while c < checknum:
        if endofline[:4] == '<!--':
            endofline = endofline[4:]
            if '<!--' in endofline:
                error = 'Problem in getextraconditions()'
                error2 = 'Too many instances of \'<!--\' in line in favourites file'
                error3 = ('File is %s'% favouritesfile)
                error4 = ('Problem line: %s'% line)
                errormessage()
            else:
                c = checknum + 1
        else:
            endofline = endofline[1:]
            c = c + 1
    if not c > checknum:
        error = 'Problem in getextraconditions()'
        error2 = 'Too many instances of \'<!--\' in line in favourites file'
        error3 = ('<!-- not found in line: %s'% line)
        errormessage()    
    # get rid of '-->' - generate an error if '-->' appears more than once or is not the last 3 characters of endofline
    if not endofline[-3:] == '-->':
        error = 'Problem in getextraconditions()'
        error2 = '\'-->\' is missing from the end of a line'
        error3 = ('File is %s'% favouritesfile)
        error4 = ('Problem line: %s'% line)
        errormessage()
    endofline = endofline[:-3]
    if '-->' in endofline:
        error = 'Problem in getextraconditions()'
        error2 = '\'-->\' is present more than once in a line'
        error3 = ('File is %s'% favouritesfile)
        error4 = ('Problem line: %s'% line)
        errormessage()
    # now we have a stripped endofline containing all extraconditions
    # checking
    print 'Stripped endofline to process is %s'% endofline
    # Looking for '<onclick>*</onclick>' and / or '<visible>*</visible>' separated by commas (and space)
    extras = []
    # use double commas to split!
    extras = endofline.split(',, ')
    # checking
    print 'extras = %s'% extras
    numberofextras = len(extras)
    p = 0
    while p < numberofextras:
        extratoadd = 'none'
        testextra = extras[p]
        if testextra[:9] == '<onclick>':
            extratoadd = testextra
        elif testextra[:9] == '<visible>':
            extratoadd = testextra
        if not extratoadd == 'none':
            if extracondition1 == 'false':
                extracondition1 = extratoadd + '\n'
                # checking
                print ('extracondition1 set as %s'% extracondition1)
            elif extracondition2 == 'false':
                extracondition2 = extratoadd + '\n'
                # checking
                print ('extracondition2 set as %s'% extracondition2)
            elif extracondition3 == 'false':
                extracondition3 = extratoadd + '\n'
            elif extracondition4 == 'false':
                extracondition4 = extratoadd + '\n'                        
            elif extracondition5 == 'false':
                extracondition5 = extratoadd + '\n'
            else:
                extracondition6 = extratoadd + '\n'
        else:
            # testextra isn't a valid <onclick> or <visible> entry.  Log and ignore
            logmessage = 'Issue in getextracondition()'
            logmessage2 = 'substring in line in favourites isn\'t a valid extra'
            logmessage3 = 'File is %s'% favouritesfile
            logmessage4 = 'Problem line: %s'% line
            printlog()
        p = p + 1
    if not extracondition1 == 'false':
        extraconditionsexist = 'true'
    
    
   
def scriptfavtoactwin():
    global error, error2, str, favslist, favsnumber, favsfolder
    print 'running scriptfavtoactwin()'
    start = ' '
    stop = ')'
    option = (str.split(start))[1].split(stop)[0]
    # check if 'option' favourites file exists - if it does get the window number from the last line
    print ('option is %s'% option)
    c = 0
    filename = 'none'
#    message = 'none'
    favsnumber = len(favslist)
    print ('favsnumber is %d'% favsnumber)
    while c < favsnumber:
        checkfav = favslist[c]
        print ('checkfav is %s'% checkfav)
        if checkfav == option:
            filename = checkfav
            print ('filename is %s'% filename)
            c = c + favsnumber
        c = c + 1
    if not filename == 'none':
        file = os.path.join(favsfolder, filename, 'favourites.xml')
        f = open(file,"r")            
        lines = f.readlines()
        lastline = lines[-1]
        if lastline[:12] == '<!--name is ':
            start = '<!--name is '
            end = '-->'
            fullname = (lastline.split(start))[1].split(end)[0]
            windowid = fullname[-4:]
            if windowid.isdigit():
                str = ('RunScript(special://userdata/smashing/smashingfavourites/scripts/automatedscripts/opendialog.py, %s)'% windowid)  # run script to give history             
#                str = ('ActivateWindow(%s)'% windowid)             # original version, direct opening > no history
                print ('str changed to %s'% str)                
            else:
                error2 = ('Problem with windowid in %s.  It was not identified as a digit'% file)
        else:
            error2 = ('Problem with last line in %s.  The name format was not found to be correct'% file)
    else:
        error2 = ('No folder matching %s was found in the favourites folders.'% option)
    if not error2 == 'none':
        error = 'problem running scriptfavtoactwin function.'
        print error
        print error2
        errormessage()
        
# get rid of funny formatting
def unescape():
    global str
    print 'running unescape()'
    str = str.replace("&lt;","<")
    str = str.replace("&gt;",">")
    str = str.replace("&quot;","\"")
    str = str.replace("&amp;","&")        
        
# list the files (lists) to process               
def listtasks():
    global listcontents, linenumber, liststorun, tasks, tasknumber
    print 'running listtasks()'
    listcontents = os.listdir(listfolder)
    liststorun = []
    num = len(listcontents)
    if num == 0:
        error = 'Problem in listtasks() function'
        error2 = ('No lists found in list folder (%s)'% listfolder)
        errormessage()
    c = 0
    while c < num:
        test = listcontents[c]
        testpath = os.path.join(listfolder, test)
        if os.path.isfile(testpath):
            liststorun.append(test)
        c = c + 1
    tasks = len(liststorun)
    tasknumber = 0
    print ('contents are %s'% listcontents)
    print ('liststorun are %s'% liststorun)
    print ('tasknumber is %s'% tasknumber)
    openlist()        

def openlist():
    global tasknumber, tasks, listname, listfile, oldlistfile, processedlist
    print 'running openlist()'
    if tasknumber < tasks:
        listname = liststorun[tasknumber]
        listfile = os.path.join(listfolder, listname)
        oldlistfile = os.path.join(oldlistfolder, listname)
        processedlist = os.path.join(workinglistfolder, listname)
        tasknumber = tasknumber + 1
        #test
        print ('listname is %s'% listname)
        print ('listfile is %s'% listfile)                       
        print ('oldlistfile is %s'% oldlistfile)    
        print ('processedlist is %s'% processedlist)   
        print ('tasknumber is %s'% tasknumber)
        readlistname()
    else:
        tidyup()

def readlistname():
    global linenumber, lines, length, name, ID, finishedfile, itemcount, icon, workinglist
    print 'running readlistname()'
    lines = file(listfile, 'r').readlines()
    length = len(lines)
    ID = 'blank'
    firstline = lines[0].rstrip()    
    #test
    print ('firstline is %s'% firstline)
    print firstline[:6]    
    # get name and id
    if not firstline[:6] == '<name>':
        error = 'Problem in readlistname()'
        error2 = ('The first line of the %s list does not correctly name the file'% name)
        errormessage()            
    start = '<name>'
    end = '</name>'
    name = (firstline.split(start))[1].split(end)[0]    
    #test
    print ('name is %s'% name)    
    # Cleanup: if name ends in '.xml' chop that off.
    # check end of name for id - if not there add it.
    if name[-4:] == '.xml':
        name = name[:-4]
        #test
        print ('name is now %s'% name)
    checkid = name[-4:]
    secondline = lines[1].rstrip()
    if checkid.isdigit():
        ID = checkid
    else:
        if not secondline[:4] == '<id>':        
            errormessage = ('The second line of the %s list does not contain a correctly formatted id'% name)
            error()         
        
    idcheck = secondline[4:-5]
        
    #test
    print ('name is %s'% name)
    print ('checkid is %s'% checkid)
    print ('idcheck is %s'% idcheck)
    print ('ID is %s'% ID)
            
    if ID == 'blank':
        ID = idcheck
        newname = name + ID
        name = newname
        print ('New name is %s'% name)
        print ('NewID is %s'% ID)
        
    # get icon name from list to use later
    thirdline = lines[2].rstrip()
    if not thirdline[:6] =='<icon>':
        errormessage = ('Problem with icon in %s list'% name)
        error()
    start = '<icon>'
    end = '</icon>'
    icon = (thirdline.split(start))[1].split(end)[0]
    
    linefour = lines[3].rstrip()
    if not linefour[:6] =='<list>':
        error = 'Problem in readlistname()'
        error2 = ('line 4 in %s list should start with <list>'% name)
        errormessage()
    linenumber = 4      # Use this to count lines as read - lines 1 to 4 (0 to 3!) have been read already, no need to process them again 
    itemcount = 1    
    workinglist = os.path.join(workinglistfolder, '%slist.xml'% name)       #(BUILDFOLDER, "lists.working", list)
    if os.path.isfile(workinglist):
        os.remove(workinglist)    
    readlistitems()

# make list to insert into Custom skin file:
def readlistitems():
    global length, linenumber, workinglist, itemcount
    print 'running readlistitems()'
    if linenumber < length:
        print 'check657'
        next = lines[linenumber].rstrip()
        checkitem = next[:6]
        print ('next is %s'% next)
        print ('checkitem is %s'% checkitem)
        if next[:6]  == '<item>':
            print 'checkpoint3'
            additem = ('					<item id="%d">\n'% itemcount)
            with open(workinglist, "a") as myfile:
                myfile.write(additem)
                print 'check667'    
            itemcount = itemcount + 1
            linenumber = linenumber + 1
            addlabel()
        elif next[:7] == '</list>':
            listtargetfolders()

    else:
        error = 'Problem in readlistitems()'
        error2 = ('Problem with list (%s): list does not follow the correct format'% name)
        errormessage()
        
def addlabel():
    global linenumber, workinglist, itemlabel
    print 'running addlabel()'
    next = lines[linenumber].rstrip()
    if next[:7] == '<label>':
        temp = next.replace('<label>', '')
        itemlabel = temp.replace('</label>', '')
        additem = ('						<label>%s</label>\n'% itemlabel)
        with open(workinglist, "a") as myfile:
            myfile.write(additem)
        linenumber = linenumber + 1
        addonclicks()
    else:
        error = 'Problem with addlabel()'
        error2 = ('Problem with addlabel function in %s list'% name)
        errormessage()

def addonclicks():
    global linenumber, ID, workinglist, error, error2
    print 'running addonclicks()'
    next = lines[linenumber].rstrip()
    if next[:9] == '<onclick>':
        linenumber = linenumber + 1
        start = '<onclick>'
        end = '</onclick>'
        click = (next.split(start))[1].split(end)[0]
        print ('click is %s'% click) 
        if not click == 'notclose':
            if not itemlabel == 'Previous Menu':            # avoids 'on-click close dialog' on common first item (Previous Menu)
                additem1 = ('                        <onclick>Dialog.Close(%s)</onclick>\n'% ID)
            additem2 = ('                        <onclick>%s</onclick>\n'% click)
            with open(workinglist, "a") as myfile:
                if not itemlabel == 'Previous Menu':        # avoids 'on-click close dialog' on common first item (Previous Menu)
                    myfile.write(additem1)
                myfile.write(additem2)
    else:
        error = 'Problem in addonclicks()'
        error2 = ('Problem with addonclicks function in %s list'% name)
        errormessage()
    addmoreonclicks()
    
def addmoreonclicks():
    global linenumber, workinglist
    print 'running addmoreonclicks()'
    next = lines[linenumber].rstrip()
    if next[:9] == '<onclick>':
        linenumber = linenumber + 1
        start = '<onclick>'
        end = '</onclick>'
        click = (next.split(start))[1].split(end)[0]
        additem = ('                        <onclick>%s</onclick>\n'% click)
        with open(workinglist, "a") as myfile:
            myfile.write(additem)
        addmoreonclicks()
    else:
        checkvisible()

def checkvisible():
    global linenumber, workinglist
    print 'running checkvisible()'
    next = lines[linenumber].rstrip()
    if next[:9] == '<visible>':
        linenumber = linenumber + 1
        start = '<visible>'
        end = '</visible>'
        vis = (next.split(start))[1].split(end)[0]
        additem = ('                        <visible>%s</visible>\n'% vis)            
    else:
        additem = ('                        <visible>true</visible>\n')
    with open(workinglist, "a") as myfile:
        myfile.write(additem)
    if additem == ('                        <visible>true</visible>\n'):
        checkenditem()
    else:
        checkmorevisibles()
    
def checkmorevisibles():
    global linenumber, workinglist
    print 'running checkmorevisibles()'
    next = lines[linenumber].rstrip()
    if next[:9] == '<visible>':
        linenumber = linenumber + 1
        start = '<visible>'
        end = '</visible>'
        vis = (next.split(start))[1].split(end)[0]
        additem = ('                        <visible>%s</visible>\n'% vis)            
        with open(workinglist, "a") as myfile:
            myfile.write(additem)
        checkmorevisibles()
    else:
        checkenditem()

def checkenditem():
    global linenumber, workinglist, error, error2
    print 'running checkenditem()'
    next = lines[linenumber].rstrip()
    if next[:7] == '</item>':
        linenumber = linenumber + 1
        additem = '					</item>\n'
        with open(workinglist, "a") as myfile:
            myfile.write(additem)
        readlistitems()
    else:
        error = 'Problem in checkenditem()'
        error2 = ('Problem with </item> in %s list'% name)
        errormessage()

def emptyoutputfolders():
    global DELETEFOLDER
    print 'Running emptyoutputfolders()'
    check = os.listdir(mainoutputfolder)
    size = len(check)
    c = 0
    while c < size:
        outputfoldername = check[c]
        outputfolder = os.path.join(mainoutputfolder, outputfoldername)
        # checking
        print ('outputfolder is %s'% outputfolder)
        if os.path.isdir(outputfolder):
            contents = os.listdir(outputfolder)
            number = len(contents)
            if number > 0:
                DELETEFOLDER = outputfolder
                # check
                print ('DELETEFOLDER is %s'% DELETEFOLDER)
                removefolder()
        if not os.path.isdir(outputfolder):
            os.mkdir(outputfolder)
        c = c + 1
    getfavs()            

# look at different versions for different skins / resolutions
def listtargetfolders():
    global jobs, jobnumber, versionstomake, DELETEFOLDER
    print 'running listtargetfolders()'
    versionstomake = []
    num = len(targetfolders)    
    #test
    print ('num is %d'% num)    
    c = 0
    while c < num:
        test = targetfolders[c]
        testpath = os.path.join(blanksfolder, test)
        #test
        print ('test is %s'% test)
        print ('testpath is %s'% testpath)        
        if os.path.isdir(testpath):
            startfile = os.path.join(blanksfolder, test, "1Customsmashingblankstart.xml")
            print ('startfile to check is %s'% startfile)
            endfile = os.path.join(blanksfolder, test, "2Customsmashingblankend.xml")
            print ('endfile to check is %s'% endfile)
            if os.path.isfile(startfile):
                if os.path.isfile(endfile):
                    versionstomake.append(test)
                    outputfolder = os.path.join(mainoutputfolder, test)
                else:
                    printstar
                    print ('No endfile found in %s folder'% test)
                    printstar()
            else:
                printstar()
                print ('No startfile found in %s folder'% test)
                printstar()
        c = c + 1
    jobs = len(versionstomake)
    jobnumber = 0
    print ('There are %d versions to make.  They are: %s'% (jobs, versionstomake))
    makefile()
        
def makefile():
    global name, tempstart, jobs, versionstomake, jobnumber, tasknumber, error, error1
    print 'running makefile()'
    active = versionstomake[jobnumber]
    print ('active is %s'% active)
    startfile = os.path.join(blanksfolder, active, "1Customsmashingblankstart.xml")
    endfile = os.path.join(blanksfolder, active, "2Customsmashingblankend.xml")
    
    outputfolder = os.path.join(mainoutputfolder, active)
    if not os.path.isdir(outputfolder):
        os.mkdir(outputfolder)
        xbmc.sleep(300)
        if not os.path.isdir(outputfolder):
            error = 'Problem in makefile()'
            error2 = ('Could not make folder at %s'% outputfolder)
    
    finishedfile = os.path.join(mainoutputfolder, active, '%s.xml'% name)
    c = 0
    with open(tempstart, 'w') as outfile:
        with open(startfile) as infile:
            for line in infile:
                if c == 0:
                    check = line.strip()[0:5]
                    if check == '<?xml':
                        line = line.replace('Customxxxx', name)
                        c = 1
                    outfile.write(line)
                elif c == 1:
                    check = line.strip()[0:7]
                    if check == '<window':
                        line = line.replace('yyyy', ID)
                    outfile.write(line)
                    c = 2
                elif c == 2:
                    check = line.strip()[0:9]
                    if check == '<texture>':
                        line = line.replace('zzzz', icon)
                        c = 3                                               
                    outfile.write(line)                    
                elif c == 3:
                    check = line.strip()[0:8]
                    if check == '<onleft>':
                        line = line.replace('yyyy', ID)
                        c = 4
                    outfile.write(line)
                elif c ==4:
                    outfile.write(line)                 
    filenames = [tempstart, workinglist, endfile]
    with open(finishedfile, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    jobnumber = jobnumber + 1
    if jobnumber < jobs:
        makefile()
    else:
        openlist()        
        

        

        
 # remove a folder recursively
def removefolder():
    global error, error2, errornotification
    print 'running removefolder()'
    print ('DELETEFOLDER is %s'% DELETEFOLDER)
    # delete folder
    # DELETEFOLDER = the full path of the folder to be removed
    if os.path.exists(DELETEFOLDER):
        count = 0
        while count < 50:
            try:
                shutil.rmtree(DELETEFOLDER)
            except:
                pass
            print ('checking for %s'% DELETEFOLDER)
            if not os.path.exists(DELETEFOLDER):
                print 'DELETEFOLDER has been removed'
                count = count + 50
            xbmc.sleep(300)
            print 'Oh no it hasn\'t'
            count = count + 1
    if os.path.exists(DELETEFOLDER):
        error = ('Problem with removefolder() function in %s.'% thisaddon)
        error2 = ('Could not delete the folder at %s'% DELETEFOLDER)
        printstar()
        errornotification = ('Something went wrong, Could not delete %s'% DELETEFOLDER)
        errormessage()
    else:
        printstar()
        print ('%s has deleted %s'% (thisaddon, DELETEFOLDER))
        printstar()
#        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFOLDER)
    xbmc.sleep(300)        
        

def tidyup():
    print 'running tidyup()'
    junk = os.listdir(workinglistfolder)
    k = len(junk)
    c = 0
    print ('The contents of %s are:'% workinglistfolder)
    while c < k:
        print junk[c]
        delete = os.path.join(workinglistfolder, junk[c])
        os.remove(delete)
        c = c + 1
    junklists = os.listdir(listfolder)
    r = len(junklists)
    c = 0
    print 'Lists to move are:'
    while c < r:
        check = junklists[c]
        print check
        latestversion = os.path.join(listfolder, check)
        oldversion = os.path.join(oldlistfolder, check)
        print ('latest is %s'% latestversion)
        if os.path.isfile(latestversion):
            print 'latest exists'
        else:
            print 'latest does not exist'
        print ('old is %s'% oldversion)
        if os.path.isfile(oldversion):
            print 'old exists'
        else:
            print 'old does not exist'        
        if os.path.isfile(oldversion):
            os.remove(oldversion)
        if os.path.isfile(latestversion):
            os.rename(latestversion, oldversion)
        c = c + 1
    if not updateskin == 'false':
        checkforskinfolder()
    elif updateallskins == 'true':
        allskinsupdate()
    else:
        finish()
        
def allskinsupdate():
    global updateskin, outputfoldername, skinxmlfoldername, skinxmlfolder, skinfolder
    print 'Running allskinsupdate()'
    skinstoupdatefile = os.path.join(CONFIG, "skinstoupdate.txt")
    f = open(skinstoupdatefile,"r")
    lines = f.readlines()
    num = len(lines)
    c = 0
    while c < num:
        line = lines[c]
        if line[:1] == '#':
            c = c + 1
        else:
            if line[:5] == 'skin.':
                skindetails = []
                skindetails = line.split(', ')
                updateskin = skindetails[0]
                skinfolder = os.path.join(ADDONSFOLDER, updateskin)
                outputfoldername = skindetails[1]
                skinxmlfoldername = skindetails[2]
                # drop \n
                skinxmlfoldername = skinxmlfoldername.strip()
                skinxmlfolder = os.path.join(skinfolder, skinxmlfoldername)
                checkforskinfolder()
                printstar()
                printstar()
                print ('skinxmlfolder is %s'% skinxmlfolder)
                printstar()
                printstar()
        c = c + 1


def checkforskinfolder():
    global skinfolder, logmessage, error, error2, error3
    print 'Running checkforskinfolder()'
    # checking - check name of skin being updated
    print ('The skin being updated (updateskin) is %s'% updateskin)
    # Get the path to the skin folder
    skinfolder = os.path.join(ADDONSFOLDER, updateskin)
    print ('skinfolder is %s'% skinfolder)
    if not os.path.isdir(skinfolder):
        print ('No folder exists at %s'% skinfolder)
        test = os.path.join(DEFAULTADDONSFOLDER, updateskin)
        if os.path.isdir(test):
            # copy the skin into the addons folder (for editing)
            SOURCE = test
            TARGET = skinfolder
            try:
                shutil.copytree(SOURCE, TARGET)
            except:
                error = 'Problem in checkforskinfolder'
                error2 = 'Could not copy folder at %s'% SOURCE
                error3 = 'to %s'% TARGET
                errormessage()
    if os.path.isdir(skinfolder):
        skinupdate() 
    else:
        logmessage = 'Checked for presence of %s to update but no folder exists'% updateskin
        printlog()

def skinupdate():
    global error, error2, skinxmlfoldername, outputfoldername, reloadskin
    printstar()
    printstar()
    print 'Running skinupdate()'
    print ('updateallskins = %s'% updateallskins)
    print ('special://skin path is %s'% activeskin)
    print ('skinfolder is %s'% skinfolder)
    printstar()
    printstar()
    # check if reload skin needed
    if activeskin == skinfolder:
        reloadskin = 'true'
        printstar()
        printstar()
        print 'activeskin = skinfolder'
        print ('reloadskin is %s'% reloadskin)
        printstar()
        printstar()
#        xbmc.executebuiltin('Notification(we have, a match)')
    # check for presence of needed texture files in skinfolder/media
    texturecheck = os.path.join(skinfolder, "media", "smashingbutton-focus.png")
    if not os.path.isfile(texturecheck):
        # copy contents of CONFIG/textures into skinfolder/media
        src = os.path.join(CONFIG, "textures")
#        print ('src is %s'% src)
        for item in os.listdir(src):
#            print ('item is %s'% item)
            s = os.path.join(src, item)
#            print ('s is %s'% s)
            d = os.path.join(skinfolder, "media", item)
#            print ('d is %s'% d)
            shutil.copyfile(s, d)
         
    # read skinstoupdate.txt if not already read (in allskinsupdate)
    if updateallskins == 'false':
        x = len(updateskin)
        skinstoupdatefile = os.path.join(CONFIG, "skinstoupdate.txt")
        f = open(skinstoupdatefile,"r")
        lines = f.readlines()
        num = len(lines)
        c = 0
        while c < num:
            line = lines[c]
            if line[:1] == '#':
                c = c + 1
            else:
                if line[:x] == updateskin:
                    input = line
                    c = num + 1
                else:
                    c = c + 1
        if not c > num:
            logmessage = 'Problem in skinupdate()'
            logmessage2 = '%s skin is not found in skinstoupdate.txt'% updateskin
            printlog()
            finish()
        update = []
        update = input.split(', ')        
        outputfoldername = update[1]
        skinxmlfoldername = update[2]
        # drop \n
        skinxmlfoldername = skinxmlfoldername.strip()
        skinxmlfolder = os.path.join(skinfolder, skinxmlfoldername)
        printstar()
        printstar()
        print ('skinxmlfolder is %s'% skinxmlfolder)
        printstar()
        printstar()
#    print ('skinxmlfolder is %s'% skinxmlfolder)
    # if newcustomdialogs = true (which is the default) remove all existing custom skin dialogs from the skin folder
    if newcustomdialogs == 'true':
        listfiles = []
        customfileslist = []
        skinxmlfolder = os.path.join(skinfolder, skinxmlfoldername)
        printstar()
        printstar()
        print ('skinxmlfolder is %s'% skinxmlfolder)
        printstar()
        printstar()
        listfiles = os.listdir(skinxmlfolder)
        print 'listfiles:'
        print listfiles
        size = len(listfiles)
        d = 0
        while d < size:
            test = listfiles[d]
            print ('test is %s'% test)
            if 'Custom.smashing' in test:
                customfileslist.append(test)
            d = d + 1
        dog = len(customfileslist)
        e = 0
        while e < dog:
            filename = customfileslist[e]
            file = os.path.join(skinxmlfolder, filename)
            try:
                print ('file to delete is %s'% file)
                os.remove(file)
            except:
                error = 'Problem in skinupdate()'
                error2 = 'Could not delete file at %s'% file
                errormessage()
            if os.path.isfile(file):
                print 'bugger'
                error = 'Problem in skinupdate()'
                error2 = 'Could not delete file at %s'% file
                errormessage()			
            e = e + 1
    # copy all files from outputfolder into skinxmlfolder
    # if not removing old customxml files - need to check one by one
    outputfolder = os.path.join(mainoutputfolder, outputfoldername)
    printstar()
    printstar()
    print ('outputfolder is %s'% outputfolder)
    printstar()
    printstar()
    if not os.path.isdir(outputfolder):
        os.mkdir(outputfolder)
        xbmc.sleep(300)
        if not os.path.isdir(outputfolder):
            error = 'Problem in skinupdate()'
            error2 = ('Could not make folder at %s'% outputfolder)
    filestocopy = os.listdir(outputfolder)
    number = len(filestocopy)
    g = 0
    while g < number:
        customfilename = filestocopy[g]
        customfile = os.path.join(outputfolder, customfilename)
        if newcustomdialogs == 'false':
            existingfile = os.path.join(skinxmlfolder, customfilename)
            if os.path.isfile(existingfile):
                try:
                    os.remove(existingfile)
                except:
                    error = 'Problem in skinupdate()'
                    error2 = 'Could not remove file at %s'% existingfile
                    errormessage()
        target = os.path.join(skinxmlfolder, customfilename)
        try:
            shutil.copyfile(customfile, target)                      # copyfile - target is file, not folder
        except:
            error = 'Problem in skinupdate()'
            error2 = 'Could not copy file at %s'% customfile
            error3 = 'into %s folder'% skinxmlfolder
            errormessage()
        g = g + 1

        
def finish():
    print 'running finish()'
    if os.path.isfile(MARKER):
        os.remove(MARKER)
    if reloadskin == 'true':
        xbmc.executebuiltin('ReloadSkin()')
        xbmc.sleep(1000)
        xbmc.executebuiltin('Notification(Skin reloaded, all done)')
    else:
        xbmc.executebuiltin('Notification(Skins updated, all done)')
    exit()

    
processtime()        
# continue startup
# check MARKER stuff
# get system time
checktime()
# check if marker present - if so stop script, if not make it
checkmarkeratstart()
getoptions()
finish()


# drink beer, eat pies 
