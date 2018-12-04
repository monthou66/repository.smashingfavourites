# -*- coding: utf-8 -*-
# smashingeditaddon.py
# start with arguments:
# Possible arguments are:
# 1. sys.argv[1] = donor_id (required) (can start argument with 'donor_addonid.')  required unless started with 'choose' or no argument
# or 1. sys.argv[1] = choose
# anything labelled #* is accessible from 'choose'
#* 2. clone_id - optional, if not there the donor_id will be edited
#* 3. clone_name - required if 2 is present, absence leads to error
# 4. deletedonor - optional - delete donor addon completely after cloning
# 5. savedonor - optional - save donor addon to oldaddons and check for updates periodically
# 6. replacefiles - optional - see config file
# 7. addfiles     - optional - see config file
#* 8. force_clone - optional - clone again even if already done
#* 9. clone_version - optional - if not present clone will be made with same version as donor
# 10. donor_version - optional - if present donor addon will take this version 
# 11. new_version - optional - if present new addon will take this version (can be donor or clone if neither specced)
# 12. disable_donor - optional - if present donor will be disabled (default is leave in current state)
# 13. disable_clone - optional - if present donor will be disabled (default is leave in current state, or enabled if new clone)
# 14. enable_donor - optional - if present donor will be enabled (default is leave in current state)
# 15. enable_clone - optional - if present donor will be enabled (default is leave in current state, or enabled if new clone)
#* 16. fake_output (or fake) - optional - if present output addon will be a 'fake' addon (ie do nothing).  Default is false
# or
# sys.argv[1] = 'choose' to select options in the gui

import xbmc
import xbmcaddon
import os
import shutil
import json
import xbmcgui

choose = 'false'
donor_id = 'none'
clone_id = 'none'
clone_name = 'none'
donor_version = 'none'
clone_version = 'none'
new_version = 'none'
disable_donor = 'false'
disable_clone = 'false'
enable_donor = 'false'
enable_clone = 'false'
deletedonor = 'false'
savedonor = 'false'
replacefiles = 'false'
addfiles = 'false'
fake_output = 'false'
error = 'none'
force_clone = 'false'
donor_name = 'none'
donor_author = 'none'
donor_summary = 'none'
donor_description = 'none'
donor_disclaimer = 'none'
systemdetails = 'none'

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    
def getsystemdetails():
    global systemdetails, error
    # list possibles
    details = []
    details.append('libreelecpi')
    details.append('libreelecarm32')
    details.append('libreelecarm64')
    details.append('libreelecpc')
    details.append('windows32')
    details.append('windows64')
    details.append('android32')
    details.append('android32')
    num = len(details)
    c = 0
    while c < num:
        check = details[c]
        if xbmc.getCondVisibility('System.HasAddon(script.%s)'% check):
            systemdetails = check
            c = num
        c = c + 1
    if systemdetails == 'none':
        error = 'systemdetails script not found in getsystemdetails().  Install the appropriate script and try again.'
        errormessage()

# get the scriptname
startaddon()
getsystemdetails()

# define some places:
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))        # this is the read-only default folder
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))               # addons are normally installed in this folder
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISC, "addons")
OLDADDONS = os.path.join(SMASHINGADDONS, "oldaddons")
# MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "smashingeditaddon.pyisrunning.txt")
# define places dependent on thisaddon:
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "%sisrunning.txt"% thisaddon)






def errormessage():
    global error
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    if not error == 'none':
        print error
    printstar()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    # try marker stuff
    if os.path.exists(MARKER):
        try:
            os.remove(MARKER)
            if not os.path.exists(MARKER):
                xbmc.sleep(300)
        except:
            error = '%s file could not be deleted - startaddon() section of %s'% (MARKER, thisaddon)
            markererrormessage()
    exit()

def markererrormessage():
    printstar()
    print markererror
    printstar()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    exit()
    


def oldcheckmarkerstart():
    global error
    # try marker stuff
    if os.path.exists(MARKER):
        try:
            os.remove(MARKER)
            if not os.path.exists(MARKER):
                xbmc.sleep(300)
        except:
            error = '%s file could not be deleted - startaddon() section of %s'% (MARKER, thisaddon)
            markererrormessage()
    open(MARKER, "w").close()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

def checkmarkerstart():
    global error
    print 'running checkmarkerstart()'
    # try marker stuff
    if os.path.exists(MARKER):
        checktime()
    
    timemin = xbmc.getInfoLabel('System.Time(mm)')
    timemin = int(timemin) * 60
    timesec = xbmc.getInfoLabel('System.Time(ss)')
    timesec = int(timesec)
    time = timemin + timesec
    print ('time is %d'% time)
    marker = open(MARKER, 'w')
    marker.write("%d" % time)


def checktime():
    print 'running checktime()'
    timemin = xbmc.getInfoLabel('System.Time(mm)')
    timemin = int(timemin) * 60
    timesec = xbmc.getInfoLabel('System.Time(ss)')
    timesec = int(timesec)
    timenow = timemin + timesec   
    timefile = open(MARKER, 'r')
    filetime = timefile.read()
    timefile.close()
    filetime = int(filetime)    
    timediff = timenow - filetime
    if timediff >= 5:
        os.remove(MARKER)
    else:
        xbmc.executebuiltin('Notification(%s, present)'% MARKER)
        xbmc.sleep(5000)
        checktime()

def getarguments():
    global choose, configfile, error
    print 'runninggetarguments'
    if len(sys.argv) == 1:
        choose = 'true'
        choosedonor()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        checkfile = os.path.join(SMASHINGADDONS, thisaddon, arg)
        print ('checkfile is %s'% checkfile)
        if arg == 'choose':
            choose = 'true'
            choosedonor()
        elif os.path.exists(checkfile):
            configfile = checkfile
            readconfigfile()
        elif arg[0:11] == 'configfile.':
            filename = arg[12:0]
            configfile = os.path.join(SMASHINGADDONS, thisaddon, filename)
            print ('configfile is %s'% configfile)
            readconfigfile()
        else:
            error = 'Not enough arguments specified'
            errormessage()
    else:
        getmorearguments()
        
def readconfigfile():
    print 'running readconfigfile()'
    exit()

def getmorearguments():
    global donor_id, clone_id, clone_name, force_clone, deletedonor, savedonor, replacefiles, addfiles, error
    print 'running getmorearguments'
    # donor_id = starting point
    arg = sys.argv[1]
    if arg[0:9] == 'donor_id.':
        donor_id = arg[10:0]
    else:
        donor_id = arg
    checkdonorexists()
    num = len(sys.argv)
    c = 2
    while c < num:
        arg = sys.argv[c]
        if arg[0:9] == 'clone_id.':
            clone_id = arg[9:]
            print ('clone_id is %s'% clone_id)
        elif arg[0:11] == 'clone_name.':
            clone_name = arg[11:]
            print ('clone_name is %s'% clone_name)
        elif arg[0:14] == 'donor_version.':
            new_version = arg[14:]
#            print ('donor_version is %s'% donor_version)
        elif arg[0:14] == 'clone_version.':
            new_version = arg[14:]
#            print ('clone_version is %s'% clone_version)
        elif arg[0:12] == 'new_version.':
            new_version = arg[12:]
#            print ('new_version is %s'% new_version)
        elif arg == 'disable_donor':
            disable_donor = 'true'
#            print ('disable_donor is %s'% disable_donor)
        elif arg == 'enable_donor':
            enable_donor = 'true'
#            print ('enable_donor is %s'% enable_donor)
        elif arg == 'disable_clone':
            disable_clone = 'true'
#            print ('disable_clone is %s'% disable_clone)
        elif arg == 'enable_clone':
            enable_clone = 'true'
#            print ('enable_clone is %s'% enable_clone)
        elif sys.argv[c] == 'force':
            force_clone = 'true'
#            print ('force_clone is %s'% force_clone)
        elif sys.argv[c] == 'force_clone':
            force_clone = 'true'
#            print ('force_clone is %s'% force_clone)
        elif sys.argv[c] == 'deletedonor':
            deletedonor = 'true'
#            print ('deletedonor is %s'% deletedonor)
        elif sys.argv[c] == 'savedonor':
            savedonor = 'true'
#            print ('savedonor is %s'% savedonor)
        elif sys.argv[c] == 'replacefiles':
            replacefiles = 'true'
#            print ('replacefiles is %s'% replacefiles)
        elif sys.argv[c] == 'addfiles':
            addfiles = 'true'
#            print ('addfiles is %s'% addfiles)
        elif sys.argv[c] == 'fake':
            fake_output = 'true'
#            print ('fake_output is %s'% fake_output)
        elif sys.argv[c] == 'fake_output':
            fake_output = 'true'
#            print ('fake_output is %s'% fake_output)
        else:
            error = ('%s is an invalid argument'% arg)
            c = num
            errormessage()
        c = c + 1
        
def printstuff():
    printstar()
    print 'running printstuff()'
    print ('systemdetails = %s'% systemdetails)
    print ('choose is %s'% choose)
    print ('donor_id is %s'% donor_id)
    print ('clone_id is %s'% clone_id)
    print ('clone_name is %s'% clone_name)
    print ('force_clone is %s'% force_clone)
    print ('deletedonor is %s'% deletedonor)
    print ('savedonor is %s'% savedonor)
    print ('replacefiles is %s'% replacefiles)
    print ('addfiles is %s'% addfiles)
    print ('disable_donor is %s'% disable_donor)
    print ('enable_donor is %s'% enable_donor)
    print ('disable_clone is %s'% disable_clone)
    print ('enable_clone is %s'% enable_clone)
    print ('force_clone is %s'% force_clone)
    print ('fake_output is %s'% fake_output)
    print ('error is %s'% error)

#    xbmc.executebuiltin('Notification(%s, has finished - check the log)'% thisaddon)
        
def checkdonorexists():
    global donor_id, error
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % donor_id):
        ADDONXML = os.path.join(ADDONSFOLDER, donor_id, "addon.xml")
        if not os.path.exists(ADDONXML):
            ADDONXML = os.path.join(DEFAULTADDONSFOLDER, donor_id, "addon.xml")
            if not os.path.exists(ADDONXML):
                error = ('Cannot find donor_id: %s'% donor_id)
                errormessage()

def chooseoptionsone():
    global error
    print 'running chooseoptionsone()'
#    edit = 
#    clone = 
    
    


    
def choosedonor():
    global donor_id, addonfolders, error
    print 'running choosedonor()'
    # Generate list of addon folders:
    addonfolders = []
    list = []
    list = os.listdir(ADDONSFOLDER)
    for d in list:
        if not d == 'packages' and not d == 'temp':
            addonfolders.append(d)
    list = os.listdir(DEFAULTADDONSFOLDER)
    for d in list:
        if not d == 'packages' and not d == 'temp':
            if d not in addonfolders:
                addonfolders.append(d)
    # sort list alphabetically
    addonfolders.sort()
    # check:
    print addonfolders
    print 'done'
    # choose addon to clone:
    CHOOSE = xbmcgui.Dialog().select("Choose an addon to clone:", addonfolders)
    if not CHOOSE == -1:
        donor_id = addonfolders[CHOOSE]
        chooseclone()
    else:
        error = 'Script cancelled by user'
        errormessage()

def chooseclone():
    global clone_id, clone_name, force_clone, error
    print 'running chooseclone()'
    
    # get clone_id
    keyboard = xbmc.Keyboard("", "Enter cloned addon id", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        clone_id = keyboard.getText()
        yesnowindow = xbmcgui.Dialog().yesno('New clone id entered is', clone_id, "", "Click Yes to proceed")
        if not yesnowindow:
            error = 'Script cancelled by user'
            errormessage()
    # check if clone_id already exists
    if clone_id in addonfolders:
        yesnowindow = xbmcgui.Dialog().yesno('New clone id already exists',"", "Click Yes to overwrite it")
        if not yesnowindow:
            error = 'Script cancelled by user'
            errormessage()
        else:
            force_clone = 'true'        
        
    # get clone_name
    keyboard = xbmc.Keyboard("", "Enter cloned addon name", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        clone_name = keyboard.getText()
        yesnowindow = xbmcgui.Dialog().yesno('New clone name entered is', clone_name, "", "Click Yes to proceed")
        if not yesnowindow:
            error = 'Script cancelled by user'
            errormessage()    
   
#    print ('donor_id is %s'% donor_id)
#    print ('clone_id is %s'% clone_id)    
#    print ('clone_name is %s'% clone_name) 

    if clone_id == 'none':
        error = 'Script cancelled by user'
        errormessage()        
    if clone_name == 'none':
        error = 'Script cancelled by user'
        errormessage()
        
def getdonorpathandversion():
    global source_donor, donor_path, donor_version, donor_xml
    print 'running getdonorpathandversion()'
    source_donor = 'Results from xbmcaddon.getAddonInfo:'
# only works if addon is enabled
    if xbmc.getCondVisibility('System.HasAddon(%s)' % donor_id):
        addon  = xbmcaddon.Addon(id='%s'% donor_id)
        donor_path = addon.getAddonInfo('path')
        donor_version = addon.getAddonInfo('version')
        donor_xml = os.path.join(donor_path, 'addon.xml')
        print ('donor_version is %s'% donor_version)
    else:
        getdonorpathandversionfromxml()        

def getdonorpathandversionfromxml():
    global source_donor, donor_path, donor_version, donor_xml, error
    print 'running getdonorpathandversionfromxml()'
    source_donor = 'Results from looking for donor addon folder and reading addon.xml:'   
    checkpath = os.path.join(ADDONSFOLDER, donor_id)      # addons are normally installed in this folder
    alternatepath = os.path.join(DEFAULTADDONSFOLDER, donor_id)  # this is the read-only default folder; addon will be here if present on install and not updated
    print 'check401'
    if os.path.exists(checkpath):
        donor_path = checkpath
    elif os.path.exists(alternatepath):
        donor_path = alternatepath
    donor_xml = os.path.join(donor_path, 'addon.xml')
    print 'check407'
    if not os.path.exists(donor_xml):
        error = ('Addon path not found for %s'% donor_id)
        errormessage()
    # check
    print ('Check - donor_xml is at %s'% donor_xml)
    
    with open(donor_xml, 'r') as myfile:
        lines = myfile.readlines()
        c = 2
        while c < 5:
            checkline = lines[c]
            print ('checkline is %s'% checkline)
            if 'version' in checkline:
                start = 'version="'
                end = '"'           
                donor_version = (checkline.split(start))[1].split(end)[0]
                print ('donor_version is %s'% donor_version)
                c = 5
            else:
                c = c + 1
        if donor_version == 'none':
            error = ('Could not get %s addon version from addon.xml'% donor_id)
            errormessage()
        
def choosecloneversion():
    global clone_version, error
    print 'running chooseversion()'
    INTRO = ('The donor addon is version %s'% donor_version)
    A = 'Use the same addon version in the clone'
    B = 'Input a different addon version for the clone'
    Q = 'Stop the script'
    LIST = [A,B,Q]
    OPTION = xbmcgui.Dialog().select(INTRO, LIST)
    print ('OPTION is %s'% OPTION)
    if OPTION == 0:
        clone_id = donor_id
    elif OPTION == 2:
        error = 'Quit option selected in choosecloneversion()'
        errormessage()
    elif OPTION == 1:
        dialog = xbmcgui.Dialog()
        
        clone_version = dialog.input('Input new addon version', type=xbmcgui.INPUT_ALPHANUM)
#        version = dialog.input('Input new addon version', type=xbmcgui.INPUT_NUMERIC)    
    
#        version = xbmcgui.Dialog().numeric('Input new addon version')
#        clone_version = str(version)
        print ('clone_version is %s'% clone_version)
        printstuff()
        exit()
    
    
    
    
    else:
        error = 'No option selected in choosecloneversion()'
        errormessage()
        

def getclonepathandversion():
    global source_clone, clone_path, clone_version
    print 'running getclonepathandversion()'
    source_clone = 'Results from xbmcaddon.getAddonInfo:'
# only works if addon is enabled
    if xbmc.getCondVisibility('System.HasAddon(%s)' % clone_id):
        addon  = xbmcaddon.Addon(id='%s'% clone_id)
        clone_path = addon.getAddonInfo('path')
        clone_version = addon.getAddonInfo('version')
        outputpathandversion()
    else:
        getclonepathandversionfromxml()

def getclonepathandversionfromxml():
    global source_clone, clone_path, clone_version, clone_xml, error
    print 'running getclonepathandversionfromxml()'
    source_clone = 'Results from looking for clone addon folder and reading addon.xml:'   
    clone_path = os.path.join(ADDONSFOLDER, clone_id)      # addons are normally installed in this folder
    clone_xml = os.path.join(clone_path, 'addon.xml')
    if not os.path.exists(clone_xml):
        clone_version = 'not installed yet'
        outputpathandversion()
    else:    
        with open(clone_xml, 'r') as myfile:
            lines = myfile.readlines()
            c = 2
            while c < 5:
                checkline = lines[c]
#                print ('checkline is %s'% checkline)
                if 'version' in checkline:
                    start = 'version="'
                    end = '"'           
                    clone_version = (checkline.split(start))[1].split(end)[0]
                    c = 5
                    outputpathandversion()
                else:
                    c = c + 1
            if clone_version == 'none':
                error = ('Could not get %s addon version from addon.xml'% clone_id)
                errormessage()
    
def outputpathandversion():
    global message
    print 'running outputpathandversion()'
    printstar()
    print ('Running %s'% thisaddon)
    print ('Donor addon is %s'% donor_id)
    print source_donor
    print ('%s path is %s'% (donor_id, donor_path))
    print ('%s version is %s'% (donor_id, donor_version))
    print ('clone addon is %s (%s)'% (clone_name, clone_id))
    print source_clone
    print ('%s path is %s'% (clone_id, clone_path))
    print ('%s version is %s'% (clone_id, clone_version))
    # if versions match there's nothing to do:
    if not force_clone == 'true':
        if donor_version == clone_version:
            message = ('%s and %s are both version %s.  No need to update'% (donor_id, clone_id, donor_version))
            finish()
        printstar()
#    checking
    print 'finished outputpathandversion'
    print ('choose is %s'% choose)
    
def cleanup():
    global OLDDLLSTODELETE, OLDCLONE, tempfolder
    print 'running cleanup()'
    OLDDLLSTODELETE = os.path.join(OLDADDONS, "temp", clone_id)
    OLDCLONE = os.path.join(OLDADDONS, clone_id)
    if os.path.exists(OLDDLLSTODELETE):
        removeolddlls()
    else:
        tempfolder = os.path.join(OLDDLLSTODELETE, '1')    
    if os.path.exists(OLDCLONE):
        deleteoldclone()
    if os.path.exists(clone_path):
        moveclonetooldclone()

def removeolddlls():
    global tempfolder
    print 'running removeolddlls()'
    try:
        shutil.rmtree(OLDDLLSTODELETE)
        if not os.path.exists(OLDDLLSTODELETE):
            tempfolder = os.path.join(OLDDLLSTODELETE, '1')
            print ('%s folder deleted'% OLDDLLSTODELETE)
    except:
        print ('Could not delete %s folder'% OLDDLLSTODELETE)
        c = 1
        while c < 20:        
            num = str(c)
            OLDCLONEFOLDER = os.path.join(OLDDLLSTODELETE, num)
            if os.path.exists(OLDCLONEFOLDER):
                try:
                    shutil.rmtree(OLDCLONEFOLDER)
                    if not os.path.exists(OLDCLONEFOLDER):
                        temp = c
                        print ('%s folder has been deleted'% OLDCLONEFOLDER)
                    else:
                        print ('Failed to delete %s folder'% OLDCLONEFOLDER)
                        temp = c + 1
                except:
                    print ('Failed to delete %s folder'% OLDCLONEFOLDER)
                    temp = c + 1
            else:
                print ('No folder found at %s'% OLDCLONEFOLDER)
            c = c + 1
            tempfolder = os.path.join(OLDDLLSTODELETE, temp)
    
def deleteoldclone():
    global error
    print 'running deleteoldclone()'
    OLDCLONEDLL = os.path.join(OLDCLONE, '%s.dll'% clone_id)
    if os.path.exists(OLDCLONE):
        try:
            shutil.rmtree(OLDCLONE)
        except:
            if os.path.exists(OLDCLONEDLL):
                if not os.path.exists(tempfolder):
                    os.makedirs(tempfolder)
                    MOVED = os.path.join(tempfolder, '%s.dll'% clone_id)
                try:
                    os.rename(OLDCLONEDLL, MOVED)
                    if os.path.exists(MOVED):
                        try:
                            shutil.rmtree(OLDCLONE)
                        except:
                            error = ('Cannot delete %s'% OLDCLONEDLL)
                            errormessage()
                except:
                    error = ('Cannot delete %s'% OLDCLONEDLL)
                    errormessage()
    # try to delete OLDDLLSTODELETE (OLDADDONS, "temp", clone_id) folder:
    if os.path.exists(OLDDLLSTODELETE):
        try:
            shutil.rmtree(OLDDLLSTODELETE)
            print ('%s folder deleted'% OLDDLLSTODELETE)
        except:
            print ('%s folder could not be deleted.'% OLDDLLSTODELETE)
    
def moveclonetooldclone():
    print 'running moveclonetooldclone()'
    if xbmc.getCondVisibility('System.HasAddon(%s)' % clone_id):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % clone_id)
        xbmc.sleep(2000)        
    if os.path.exists(clone_path):
        try:
            shutil.move(clone_path, OLDCLONE)
        except:
            xbmc.sleep(300)
            try:
                shutil.move(clone_path, OLDCLONE)
            except:
                error = ('Cannot move %s folder to %s'% (clone_path, clone_path))
                errormessage()
        
def startclone():
    # copy donor addon to clone folder:
    print 'running startclone()'
    xbmc.executebuiltin('Action(UpdateLocalAddons)')
    xbmc.sleep(300) 
    shutil.copytree(donor_path, clone_path)
    # start editing:
    # Work through all files in the folder.  If they end in .py or .xml do a substitution - clone_id for donor_id.
    # Extras - addon.xml: change addon name, change provider, don't change .dll referred to if binary addon
#    testlistdir()
    listclone()

def listclone():
    global file, filepath, subpath
    print 'running listclone()'
    list = []
    list = os.listdir(clone_path)
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isfile(e):
            file = d
            filepath = e
            selectfiles()
        elif os.path.isdir(e):
            subpath = e
            listsub1()
            
def listsub1():
    global file, filepath, subpath2
    print 'running listsub1()'
    list = []
    list = os.listdir(subpath)
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isfile(e):
            file = d
            filepath = e
            selectfiles()
        elif os.path.isdir(e):
            subpath2 = e
            listsub2()        

def listsub2():
    global file, filepath, subpath3
    print 'running listsub2()'
    list = []
    list = os.listdir(subpath2)
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isfile(e):
            file = d
            filepath = e
            selectfiles()
        elif os.path.isdir(e):
            subpath3 = e
            listsub3()

def listsub3():
    global file, filepath, subpath4
    print 'running listsub3()'
    list = []
    list = os.listdir(subpath3)
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isfile(e):
            file = d
            filepath = e
            selectfiles()
        elif os.path.isdir(e):
            subpath4 = e
            listsub4()
            
def listsub4():
    global file, filepath
    print 'running listsub4()'
    list = []
    list = os.listdir(subpath4)
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isfile(e):
            file = d
            filepath = e
            selectfiles()
        elif os.path.isdir(e):
            printstar()
            print ('Warning - Too many subdirectories in %s folder'% clone_id)
            print ('%s folder has not been processed'% e)
            printstar
            xbmcgui.Dialog().ok('Some subfolders not processed.', 'Check your log for details.')



def checklistclone():
    print 'running checklistclone()'
    # checking:
    printstar()
    print ('top level of %s folder:'% clone_id)
    for d in list:
        print d
    print 'Files in top level:'
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isfile(e):
            print e
    print 'Folders in top level:'
    for d in list:
        e = os.path.join(clone_path, d)
        if os.path.isdir(e):
            print e    

            
def testlistdir():
    print 'running testlistdir()'
    global file, filepath
    testpath = os.path.join(ADDONSFOLDER, 'skin.xonfluence')
    list = os.listdir(testpath)
    printstar()
    print 'top level of skin.xonfluence folder:'
    for d in list:
        print d
    print 'Files in top level:'
    for d in list:
        e = os.path.join(testpath, d)
        if os.path.isfile(e):
            print e
    print 'Folders in top level:'
    for d in list:
        e = os.path.join(testpath, d)
        if os.path.isdir(e):
            print e
            
    # testing
    file = 'addon.xml'
    filepath = os.path.join(ADDONSFOLDER, clone_id, 'addon.xml')
    editaddonxml()
    
def selectfiles():
    global file, filepath
    print 'running selectfiles()'
    if file == 'addon.xml':
        editaddonxml()
    elif file == 'addon.xml.in':
        editaddonxml()
    elif file[-3:] == 'xml':
        editfile()
    elif file[-2:]  == 'py':
        editfile()
    
def editaddonxml():
#    global file, filepath
    print 'running editaddonxml()'
    # Replace addonid in file:
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(donor_id, clone_id))    
    # Don't rename .dll so change back here!):
    newdllname = ('%s.dll'% clone_id)
    olddllname = ('%s.dll'% donor_id)    
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(newdllname, olddllname))
    # get name, author, summary, description, disclaimer of donor:
    getdonordetails()
    # Replace addon name in file:    
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(donor_name, clone_name))
    # edit clone author name
    clone_author = ('Addon by %s, mucked about with by me'% donor_author)
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(donor_author, clone_author))
    # remove all but one lines for summary, description, disclaimer
    # first remove all of them    
    f = open(filepath,"r")
    lines = f.readlines()
    f.close()
    f = open(filepath,"w")
    for line in lines:
        if '<summary lang="' not in line and '<description lang="' not in line and '<disclaimer lang="' not in line:
            f.write(line)
    # now add them back in:
    f = open(filepath,"r")
    lines = f.readlines()
    f.close()
    f = open(filepath,"w")
    clone_summary = ('    <summary lang="en">Cloned version of %s: %s</summary>\n'% (donor_id, donor_summary))
    clone_description = ('    <description lang="en">Pretty much the same as %s: %s.</description>\n'% (donor_id, donor_description))
    clone_disclaimer = ('    <disclaimer lang="en">Unsurprisingly still the same as %s...%s</disclaimer>\n'% (donor_id, donor_disclaimer))
    for line in lines:
        f.write(line)
        if '<extension point="xbmc.addon.metadata">' in line:
            f.write(clone_summary)
            f.write(clone_description)
            f.write(clone_disclaimer)
    
    
def getdonordetails():
    global source, donor_name, donor_author, donor_summary, donor_description, donor_disclaimer
    print 'running getdonordetails()'
    # read from donor_xml: 

    with open(donor_xml, 'r') as myfile:
        lines = myfile.readlines()
        length = len(lines)
        print ('length = %d'% length)
        c = 0
        while c < length:
            checkline = lines[c]
#            print ('checkline is %s'% checkline)
            if ' name="' in checkline:
                start = 'name="'
                end = '"'           
                donor_name = (checkline.split(start))[1].split(end)[0]
            if 'provider-name' in checkline:
                start = 'provider-name="'
                end = '"'           
                donor_author = (checkline.split(start))[1].split(end)[0]
            elif '<summary lang="en">' in checkline:
                start = '<summary lang="en">'
                end = '</summary>'           
                donor_summary = (checkline.split(start))[1].split(end)[0]
            elif '<summary lang="en_GB">' in checkline:
                start = '<summary lang="en_GB">'
                end = '</summary>'           
                donor_summary = (checkline.split(start))[1].split(end)[0]           
            elif '<description lang="en">' in checkline:
                start = '<description lang="en">'
                end = '</description>'           
                donor_description = (checkline.split(start))[1].split(end)[0]    
            elif '<description lang="en_GB">' in checkline:
                start = '<description lang="en_GB">'
                end = '</description>'           
                donor_description = (checkline.split(start))[1].split(end)[0]
            elif '<disclaimer lang="en">' in checkline:
                start = '<disclaimer lang="en">'
                end = '</disclaimer>'           
                donor_disclaimer = (checkline.split(start))[1].split(end)[0]
            elif '<disclaimer lang="en_GB">' in checkline:
                start = '<disclaimer lang="en_GB">'
                end = '</disclaimer>'           
                donor_disclaimer = (checkline.split(start))[1].split(end)[0]
            c = c + 1
    print ('donor_name is %s'% donor_name)
    print ('donor_author is %s'% donor_author)            
    print ('donor_summary is %s'% donor_summary)
    print ('donor_description is %s'% donor_description)
    print ('donor_disclaimer is %s'% donor_disclaimer)            
    if donor_name == 'none':
        error = ('Problem in getdonordetails(): donor_name not found in %s'% donor_id)
        errormessage()
    if donor_author == 'none':
        error = ('Problem in getdonordetails(): donor_author not found in %s'% donor_id)
        errormessage()
#    if donor_summary == 'none':
#        error = ('Problem in getdonordetails(): donor_summary not found in %s'% donor_id)
#        errormessage()
#    if donor_description == 'none':
#        error = ('Problem in getdonordetails(): donor_description not found in %s'% donor_id)
#        errormessage()
#    if donor_disclaimer == 'none':
#        error = ('Problem in getdonordetails(): donor_disclaimer not found in %s'% donor_id)
#        errormessage()


    
def editfile():
#    global file, filepath
    print 'running editfile()'
    # Replace addonid in file:
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(donor_id, clone_id))




        
def finish():
    printstar()
    print 'running finish()'
    print message
    printstar()
    if os.path.exists(MARKER):
        try:
            os.remove(MARKER)
            if not os.path.exists(MARKER):
                xbmc.sleep(300)
        except:
            error = '%s file could not be deleted - startaddon() section of %s'% (MARKER, thisaddon)
            markererrormessage()
    exit()
    
checkmarkerstart()
getarguments()
# process donor addon:
printstuff()


getdonorpathandversion()

# process clone addon:
if choose == 'true':
    print 'check912'
    choosecloneversion()
else:
    print 'check915'
    getclonepathandversion()

exit()
   
# Get rid of any existing backups and move existing addon into backup folder:
cleanup()
startclone()

message = 'All done'
finish()
# make new clone:
        
        
        
        
        
# Drink beer



