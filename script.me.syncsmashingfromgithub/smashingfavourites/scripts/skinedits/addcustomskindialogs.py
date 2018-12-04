# -*- coding: utf-8 -*-
# generic starting functions

# import
import xbmc
import os
import shutil
import sys
import distutils.dir_util
from distutils.dir_util import copy_tree

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# sources
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))        # this is the read-only default folder
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))               # addons are normally installed in this folder
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
# get info
#activeskin = xbmc.translatePath('special://skin')
#activeskin = activeskin[:-1]                    # removes backslash to match against skinfolder to check if need to reload skin
activeskin = xbmc.getSkinDir()
thisaddon = sys.argv[0]

# defaults
force = 'false'
updateallskins = 'true'
completedupdates = []
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
reloadskin = 'false'


# errors
def errormessage():
    global error, error2
    printstar()
    print 'running errormessage()'
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
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    print ('%s is stopping.'% thisaddon)
    printstar()
    exit()    

def getoptions():
    global force, updateskin, updateallskins
    size = len(sys.argv)
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
            elif d[:5] == 'skin.':
                updateskin = d
                updateallskins = 'false'
            c = c + 1

def checkskinpaths():
    global skintocheck, skinstoupdate, error
    checkpath = os.path.join(ADDONSFOLDER, skintocheck)
    if os.path.isdir(checkpath):
        skinstoupdate.append(skintocheck)
    else:
        checkdefaultpath = os.path.join(DEFAULTADDONSFOLDER, skintocheck)
        if os.path.isdir(checkdefaultpath):
            # copy the skin into the addons folder (for editing)
            SOURCE = checkdefaultpath
            TARGET = checkpath
            print ('%s is copying the %s folder so it can be edited'% (thisaddon, skintocheck))				
            try:
                shutil.copytree(SOURCE, TARGET)
            except:
                error = ('Problem copying %s to addons folder for editing'% skintocheck)
                errormessage()			
            skinstoupdate.append(skintocheck)

def removefile():
    global error, error2, DELETEFILE
    try:
        os.remove(DELETEFILE)
    except:
        pass
    if os.path.exists(DELETEFILE):
        error = ('Problem with removefile() function in %s.'% thisaddon)
        error2 = ('Could not delete the file at %s'% DELETEFILE)
        errormessage()
		
 # remove a folder recursively
def removefolder():
    global error, error2, DELETEFOLDER
    try:
         shutil.rmtree(DELETEFOLDER)
    except:
        pass
    if os.path.exists(DELETEFOLDER):
        error = ('Problem with removefolder() function in %s.'% thisaddon)
        error2 = ('Could not delete the folder at %s'% DELETEFOLDER)
        errormessage()
					
def cleanskin():
    global error, skin, DELETEFILE, DELETEFOLDER
    folder = os.path.join(ADDONSFOLDER, skin, xmlfolder)
    print 'running cleanskin()'
    check = []
    check = os.listdir(folder)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:16] == 'Custom.smashing.':
            DELETEFILE = os.path.join(folder, next)
            removefile()
        c = c + 1
    # clean up other stuff
    DELETEFILE = os.path.join(ADDONSFOLDER, skin, 'version.txt')
    if os.path.isfile(DELETEFILE):
        removefile()
    DELETEFOLDER = os.path.join(ADDONSFOLDER, skin, 'version')
    if os.path.isdir(DELETEFOLDER):
        removefolder()
    print ('Cleaned %s'% skin)
			
			
def overwrite():			
    global error, skin, completedupdates, activeskin, reloadskin
    print 'running overwrite()'
    # remove existing custom.smashing and marker files
    cleanskin()
    # copy edits into the skin folder
    SOURCE = os.path.join(DIALOGFOLDER, skin)
    TARGET = os.path.join(ADDONSFOLDER, skin)
    printstar()
    printstar()
    print ('Copying custom files for %s'% skin)
    print ('SOURCE = %s'% SOURCE)
    print ('TARGET is %s'% TARGET)
    printstar()
    printstar()
    distutils.dir_util._path_created = {}
    copy_tree(SOURCE, TARGET)
#    shutil.copytree(SOURCE, TARGET)
    completedupdates.append(skin)
    print ('Updated %s'% skin)
    if skin == activeskin:
        reloadskin = 'true'
        print ('%s is the active skin'% skin)
        print ('reloadskin is set to %s'% reloadskin)
    else:
        print ('%s is not the active skin'% skin)
        print ('reloadskin is set to %s'% reloadskin)


def checkversion():
    global skin
    # compare smashingversion with current version, update if necessary
    print ('running checkversion() for %s'% skin)
    smashingfile = os.path.join(DIALOGFOLDER, skin, "version.txt")
    with open(smashingfile, 'r') as myfile:
        smashingversion = myfile.read()
    print ('Version in smashing folder is %s'% smashingversion)
    smashingversion = int(smashingversion)
    currentfile = os.path.join(ADDONSFOLDER, skin, "version.txt")
    if os.path.isfile(currentfile):
        with open(currentfile, 'r') as myfile:
            currentversion = myfile.read()
        print ('Version in current %s folder is %s'% (skin, smashingversion))
    else:
        currentversion = 0
        print ('%s folder has not previously been edited'% skin)
	currentversion = int(currentversion)
    if smashingversion > currentversion:
        print ('Updating %s folder from smashing'% skin)
        overwrite()
    else:
        print ('%s will not be updated'% skin)
        
def finish():
    global reloadskin, completedupdates
    printstar()
    print ('running finish() in %s'% thisaddon)
    print ('reloadskin is set to %s'% reloadskin)
    total = len(completedupdates)
    if total > 0:
        print ('Skins updated: %s'% completedupdates)
    else:
        print 'No skins have been updated.'
    if reloadskin == 'true':
        xbmc.executebuiltin('ReloadSkin()')
        xbmc.sleep(1000)
        xbmc.executebuiltin('Notification(Skin reloaded, all done)')
    else:
        xbmc.executebuiltin('Notification(Skins updated, all done)')
    exit()


	
	#########################################################################################
# let's get going	
# get kodi version, check for matching folder in config, stop if not there
kodiversion = xbmc.getInfoLabel('System.BuildVersion')
kodiversion = kodiversion[:2]
printstar()
print ('%s has started'% thisaddon)
print ('kodiversion is %s' % kodiversion)
print ('The active skin is %s'% activeskin)
# find update folder
DIALOGFOLDER = os.path.join(SMASHINGFAVOURITES, "skins.forceeditfiles", kodiversion)
if not os.path.exists(DIALOGFOLDER):
    error = ('No folder exists at %s' % DIALOGFOLDER)
    errormessage()
# list skins in DIALOGFOLDER
skinlist = []
skinstoupdate = []
skinlist = os.listdir(DIALOGFOLDER)
size = len(skinlist)
if size == 0:
    error = ('No skin folders were found in %s'% DIALOGFOLDER)
    errormessage()
# list skins to edit, and copy any required skins from default addons folder
getoptions()
if updateallskins == 'false':				# ie only one skin to update
    # check whether skin has edits available
    if not updateskin in skinlist:
        error = ('%s was the skin specified to be edited'% updateskin)
        error2 = ('There are no updates available for %s in %s'% (updateskin, DIALOGFOLDER))
        errormessage()
    # check whether skin is installed, and move it if necessary  
    skintocheck = updateskin	
    checkskinpaths()
else:						# ie if doing updateall
    c = 0
    while c < size:
        skintocheck = skinlist[c]
        checkskinpaths()
        c = c + 1
# list skins to be edited
numbertoupdate = len(skinstoupdate)
if numbertoupdate == 0:
    error = 'There are no skin updates available'
    errormessage()
print ('Skins to update: %s'% skinstoupdate)
# update!
c = 0
while c < numbertoupdate:
    skin = skinstoupdate[c]
    # get folder containing .xml files
    xmlfile = os.path.join(DIALOGFOLDER, skin, "xmlfolder.txt")
    with open(xmlfile, 'r') as myfile:
        xmlfolder = myfile.read()
    if force == 'true':
        overwrite()
    else:
        checkversion()		# overwrites unless current version already present
    c = c + 1
finish()


# drink beer, eat pies 
