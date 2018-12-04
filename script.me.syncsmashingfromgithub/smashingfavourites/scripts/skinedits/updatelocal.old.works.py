# -*- coding: utf-8 -*-
# generic starting functions

# import
import xbmc
import os
import shutil
import sys
import distutils.dir_util
from distutils.dir_util import copy_tree
import socket

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# sources
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))               # addons are normally installed in this folder
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
targetdir = os.path.join(SMASHINGFAVOURITES, "skineditfiles")
sourcedir = os.path.join(SMASHINGTEMP, "buildcustomskindialogs", "output")
thisaddon = sys.argv[0]

# defaults
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
force = 'false'     # force ignores extra check on skinstoupdate.txt

def getoptions():
    global force
    size = len(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'force':
            force = 'true'
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

def removefile():
    global error, error2, DELETEFILE
    if not os.path.isfile(DELETEFILE):
        printstar()
        printstar()
        print 'Running deletefile'
        print ('Tried to delete %s'% DELETEFILE)
        print 'File not found'
        printstar()
        printstar()
    try:
        os.remove(DELETEFILE)
    except:
        pass
    if os.path.exists(DELETEFILE):
        error = ('Problem with removefile() function in %s.'% thisaddon)
        error2 = ('Could not delete the file at %s'% DELETEFILE)
        errormessage()
        
def copyfile():
    global error, error2
    print 'running copyfile()'
    if not os.path.isfile(SOURCE):
        error = 'Problem with copyfile() function'
        error2 = ('SOURCE file (%s) does not exist'% SOURCE)
        errormessage()    
    if os.path.isfile(TARGET):
        error = ('TARGET file (%s) already exists'% TARGET)
        error2 = 'This should have already been deleted'
        errormessage()
    try:
        shutil.copyfile(SOURCE, TARGET)
    except:
        error = 'Problem with copyfile() function'
        error2 = ('Copyfile failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
        
def checkskinupdatetext():
    global skin, skinupdatesource, skinupdatexmlfolder, skinstoupdatefile, outputfoldername, skinxmlfoldername, error, error2
    print ('running checkskinupdatetext() for %s'% skin)
    skinstoupdatefile = os.path.join(SMASHINGFAVOURITES, "scripts", "skinedits", "config", kodiversion, "skinstoupdate.txt")
    if not os.path.isfile(skinstoupdatefile):
        error = ('No file found at %s'% skinstoupdatefile)
        error2 = 'Script can still run with force enabled'
        errormessage()
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
                if updateskin == skin:
                    outputfoldername = skindetails[1]
                    skinxmlfoldername = skindetails[2]
                    # drop \n
                    skinxmlfoldername = skinxmlfoldername.strip()
                    c = 500
        c = c + 1
    if c < 500:
        error = ('Skin details for %s were not found in %s'% (skin, skinstoupdatefile))
        errormessage()
        
def readtextfile():
    global skin, txtfile, output, error
    print ('running readtextfile() for %s - checking %s'% (skin, txtfile))
    if not os.path.isfile(txtfile):
        error = ('No file found at %s'% txtfile)
        errormessage()
    with open(txtfile, 'r') as myfile:
        output = myfile.read()
        print ('Output of %s is: %s'% (txtfile, output))
        
def finish():
    printstar()
    print ('%s is shutting down'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Skin folders updated, all done)')
    exit()


	
	#########################################################################################
# let's get going	
# get kodi version
kodiversion = xbmc.getInfoLabel('System.BuildVersion')
kodiversion = kodiversion[:2]
getoptions()
printstar()
print ('%s has started'% thisaddon)
print ('kodiversion is %s' % kodiversion)
print ('force value is %s'% force)
printstar()
# check for presence of files in sourcedir - if that's empty or not there stop script
checksource = os.path.join(sourcedir, "estuary")
print 'check 170'
if not os.path.isdir(checksource):
    error = ('No folder found at %s'% checksource)
    errormessage()
checklist = os.listdir(checksource)
chksz = len(checklist)
print 'check 176'
if chksz == 0:
    error = ('No files found in %s'% checklist)
    errormessage()
# check for expected number of files (match against smashingfavourites)
checkfavsfolder = os.path.join(SMASHINGFAVOURITES, "options")
print 'check 182'
if not os.path.isdir(checkfavsfolder):
    error = ('No folder found at %s'% checkfavsfolder)
    errormessage()
checkfavs = os.listdir(checkfavsfolder)
chkfvs = len(checkfavs)
print 'check 188'
if chksz < chkfvs:
    print ('%d files found in %s'% (chksz, checklist))
    print ('%d files found in %s'% (chkfvs, checkfavs))
    error = 'Files in smashingfavourites and smashingtemp do not match.'
    error2 = ('Check the folders at %s'% sourcedir)
    errormessage()
# check all files in checksource start with 'Custom.smashing.'
print 'check 196'
c = 0
while c < chksz:
    checkname = checklist[c]
    print 'check 200'
    if not checkname[:16] == 'Custom.smashing.':
        printstar()
        print ('%s is checking %s'% (thisaddon, checkname))
        error = ('Problem with naming of %s in %s folder'% (checkname, checksource))
        errormessage()
    c = c + 1
print 'check 207'
# check all folders in sourcedir have the same number of files (ie all processed)
cat = os.listdir(sourcedir)
catsz = len(cat)
c = 0
while c < catsz:
    bat = cat[c]
    fat = os.path.join(sourcedir, bat)
    mat = os.listdir(fat)
    batsz = len(mat)
    print 'check 217'
    if not batsz == chksz:
        print ('%s folder has %d files'% (checksource, chksz))
        print ('%s folder has %d files'% (bat, batsz))
        error = ('Problem with folders in %s'% sourcedir)
        error2 = 'Folders should have the same number of files'
        errormessage()
    c = c + 1
# Work through folders in target, delete existing 'Custom.smashing.' files and replace with new ones.
TARGETFOLDER = os.path.join(targetdir, kodiversion)
print 'check 226'
if not os.path.exists(TARGETFOLDER):
    error = ('No folder exists at %s' % TARGETFOLDER)
    errormessage()
# list skins in TARGETFOLDER
print 'check 231'
skinlist = []
skinlist = os.listdir(TARGETFOLDER)
printstar()
print 'skinlist:'
print skinlist
printstar()
size = len(skinlist)
if size == 0:
    error = ('No skin folders were found in %s'% TARGETFOLDER)
    errormessage()
print 'check 238'
d = 0
while d < size:
    skin = skinlist[d]
    skinfolder = os.path.join(TARGETFOLDER, skin)
    if os.path.isdir(skinfolder):
        txtsource = os.path.join(skinfolder, 'source.txt')
        txtversion = os.path.join(skinfolder, 'version.txt')
        txtxmlfolder = os.path.join(skinfolder, 'xmlfolder.txt')
        txtorigins = os.path.join(skinfolder, 'origins.txt')            # optional, add machine and date
        # check text files for updating info
        txtfile = txtsource
        readtextfile()
        skinsource = output
        txtfile = txtxmlfolder
        readtextfile()
        skinxmlfolder = output
        ##################################################################################
    # test skinsource and skinxmlfolder against contents of smashingfavourites/scripts/skinedits/config/version/skinstoupdate.txt
    # Ignore if run with 'force'
        if force == 'false':
            checkskinupdatetext()
            if not skinsource == outputfoldername:
                print ('skinsource is %s'% skinsource)
                print ('outputfoldername is %s'% outputfoldername)
                error = 'Name mismatch found - check this or start script with force enabled'
                errormessage()
            if not skinxmlfolder == skinxmlfoldername:
                print ('skinxmlfolder is %s'% skinxmlfolder)
                print ('skinxmlfoldername is %s'% skinxmlfoldername)
                error = 'Name mismatch found - check this or start script with force enabled'
                errormessage()
        ####################################################################################
        # getversion
        txtfile = txtversion
        readtextfile()
        skinversion = output
        # add a marker to show folder is being worked on (so if script fails during update it's obvious)
        workingmarker = os.path.join(skinfolder, 'warning-partialupdate.txt')
        marker = open(workingmarker, "w")
        marker.close()
        # Remove files and folders that need to be updated.
        DELETEFILE = txtversion
        removefile()
        DELETEFILE = os.path.join(skinfolder, "version", skinversion)
        removefile()
        # go through xml files
        targetxmlfolder = os.path.join(skinfolder, skinxmlfolder)
        fox = os.listdir(targetxmlfolder)
        box = len(fox)
        c = 0
        while c < box:
            socks = fox[c]
            if socks[:16] == 'Custom.smashing.':
                if not socks[:19] == 'Custom.smashing.aaa':
                    DELETEFILE = os.path.join(targetxmlfolder, socks)
                    removefile()
            c = c + 1
        # copy .xml files to target
        sourcexmlfolder = os.path.join(sourcedir, skinxmlfolder)
        print ('sourcexmlfolder is %s'% sourcexmlfolder)
    #    exit()    
        sourcefolder = os.path.join(sourcedir, skinsource) 
        print ('sourcefolder is %s'% sourcefolder)    
        cox = os.listdir(sourcefolder)
        sox = len(cox)
        c = 0
        while c < sox:
            pox = cox[c]
            SOURCE = os.path.join(sourcefolder, pox)
            print ('SOURCE is %s'% SOURCE)
            TARGET = os.path.join(targetxmlfolder, pox)
            print ('TARGET is %s'% TARGET)
            copyfile()
            c = c + 1
        # make version files and origins file
        skinversion = int(skinversion)
        skinversion = skinversion + 1
        skinversion = str(skinversion)  
        print ('Making new version files for %s - New version is %s'% (skin, skinversion))
        newversionfile = open(txtversion, "w")
        newversionfile.write(skinversion)
        newversionfile.close()
        versionfiletoo = os.path.join(skinfolder, "version", skinversion)  
        othernewversionfile = open(versionfiletoo, "w")
        othernewversionfile.close()
        # make source text
        host = socket.gethostname()
        date = xbmc.getInfoLabel('System.Date(dd-mm-yy)').strip()
        txtorigin = os.path.join(skinfolder, 'origin.txt')
        filessource = open(txtorigin, "w")
        filessource.write('Custom.smashing files source:\n')
        filessource.write('\n')
        filessource.write('Made on %s\n'% host)
        filessource.write('Running kodi version %s\n'% kodiversion)
        filessource.write('Date: %s\n'% date)
        filessource.close()
        # remove marker file
        DELETEFILE = workingmarker
        removefile()
        # and on to the next skin
    d = d + 1


finish()


# drink beer, eat pies 
