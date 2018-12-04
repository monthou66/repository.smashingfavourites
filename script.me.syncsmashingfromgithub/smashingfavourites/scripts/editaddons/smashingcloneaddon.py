# -*- coding: utf-8 -*-
# smashingcloneaddon.py
# start with arguments:
# sys.argv[1] = donor addon id
# sys.argv[2] = clone addon id
# sys.argv[3] = clone addon name
# or
# sys.argv[1] = 'choose' to select options in the gui

import xbmc
import xbmcaddon
import os
import shutil
import json
import xbmcgui

# define some places:
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))        # this is the read-only default folder
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))               # addons are normally installed in this folder
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISC, "addons")
OLDADDONS = os.path.join(SMASHINGADDONS, "oldaddons")
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "smashingcloneaddon.pyisrunning.txt")

donor_id = 'none'
clone_id = 'not found'
clone_name = 'not found'
donor_version = 'not found'
clone_version = 'not found'
error = 'non-specific'
force_clone = 'false'
donor_name = 'not found'
donor_author = 'not found'
donor_summary = 'not found'
donor_description = 'not found'
donor_disclaimer = 'not found'

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def errormessage():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    if not error == 'non-specific':
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
    
def startaddon():
    global thisaddon, error
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    
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

def getarguments():
    global donor_id, clone_id, clone_name, force_clone, error
    print 'running getarguments'
    if len(sys.argv) > 3:
        donor_id = sys.argv[1]
        clone_id = sys.argv[2]
        clone_name = sys.argv[3]
    else:
        if len(sys.argv) > 1:
            if sys.argv[1] == 'choose':
                choosedonor()
        else:
            error = 'Not enough arguments'
            errormessage()
    if len(sys.argv) > 4:
        if sys.argv[4] == 'force':
        # check
            print sys.argv[4]
            force_clone = 'true'
            print ('force_clone is %s'% force_clone)
            
def choosedonor():
    global donor_id, addonfolders, error
    print 'running chooseoptions'
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
    global clone_id, clone_name, error
    print 'running chooseclone'
    
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
        
    # get clone_name
    keyboard = xbmc.Keyboard("", "Enter cloned addon name", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        clone_name = keyboard.getText()
        yesnowindow = xbmcgui.Dialog().yesno('New clone name entered is', clone_name, "", "Click Yes to proceed")
        if not yesnowindow:
            error = 'Script cancelled by user'
            errormessage()    
   
    print ('donor_id is %s'% donor_id)
    print ('clone_id is %s'% clone_id)    
    print ('clone_name is %s'% clone_name) 

    if clone_id == 'not found':
        error = 'Script cancelled by user'
        errormessage()        
    if clone_name == 'not found':
        error = 'Script cancelled by user'
        errormessage()
        
def getdonorpathandversion():
    global source_donor, donor_path, donor_version, donor_xml
    print 'running getdonorpathandversion'
    source_donor = 'Results from xbmcaddon.getAddonInfo:'
# only works if addon is enabled
    if xbmc.getCondVisibility('System.HasAddon(%s)' % donor_id):
        addon  = xbmcaddon.Addon(id='%s'% donor_id)
        donor_path = addon.getAddonInfo('path')
        donor_version = addon.getAddonInfo('version')
        donor_xml = os.path.join(donor_path, 'addon.xml')
    else:
        getdonorpathandversionfromxml()        

def getdonorpathandversionfromxml():
    global source_donor, donor_path, donor_version, donor_xml, error
    print 'running getdonorpathandversionfromxml'
    source_donor = 'Results from looking for donor addon folder and reading addon.xml:'   
    checkpath = os.path.join(ADDONSFOLDER, donor_id)      # addons are normally installed in this folder
    alternatepath = os.path.join(DEFAULTADDONSFOLDER, donor_id)  # this is the read-only default folder; addon will be here if present on install and not updated
    if os.path.exists(checkpath):
        donor_path = checkpath
    elif os.path.exists(alternatepath):
        donor_path = alternatepath
    donor_xml = os.path.join(donor_path, 'addon.xml')
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
                c = 5
            else:
                c = c + 1
        if donor_version == 'not found':
            error = ('Could not get %s addon version from addon.xml'% donor_id)
            errormessage()                

def getclonepathandversion():
    global source_clone, clone_path, clone_version
    print 'running getclonepathandversion'
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
    print 'running getclonepathandversionfromxml'
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
            if clone_version == 'not found':
                error = ('Could not get %s addon version from addon.xml'% clone_id)
                errormessage()
    
def outputpathandversion():
    global message
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
    
def cleanup():
    global OLDDLLSTODELETE, OLDCLONE, tempfolder
    print 'running cleanup'
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
    print 'running startclone'
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
    print 'running listclone'
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
    print 'running listsub1'
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
    print 'running listsub2'
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
    print 'running listsub3'
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
    print 'running listsub4'
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
    print 'running selectfiles'
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
    print 'running editaddonxml'
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
    print 'running getdonordetails'
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
    if donor_name == 'not found':
        error = ('Problem in getdonordetails(): donor_name not found in %s'% donor_id)
        errormessage()
    if donor_author == 'not found':
        error = ('Problem in getdonordetails(): donor_author not found in %s'% donor_id)
        errormessage()
#    if donor_summary == 'not found':
#        error = ('Problem in getdonordetails(): donor_summary not found in %s'% donor_id)
#        errormessage()
#    if donor_description == 'not found':
#        error = ('Problem in getdonordetails(): donor_description not found in %s'% donor_id)
#        errormessage()
#    if donor_disclaimer == 'not found':
#        error = ('Problem in getdonordetails(): donor_disclaimer not found in %s'% donor_id)
#        errormessage()


    
def editfile():
#    global file, filepath
    print 'running editfile'
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
    
startaddon()
getarguments()
# process donor addon:
getdonorpathandversion()
# process clone addon:
getclonepathandversion()

   
# Get rid of any existing backups and move existing addon into backup folder:
cleanup()
startclone()

message = 'All done'
finish()
# make new clone:
        
        
        
        
        
# Drink beer



