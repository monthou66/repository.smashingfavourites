# -*- coding: utf-8 -*-
# smashingtosimple.py - updates the saved folders in userdata/addon_data/simplefavs

# import
import xbmc
import xbmcgui
import os
import shutil
import sys
import socket

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
simplefavourites = 'plugin.program.simple.favourites'
thisaddon = sys.argv[0]

# sources
USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
tempfolder = os.path.join(SMASHINGTEMP, "buildsimplefromsmashingfavs")
simpledir = os.path.join(ADDONDATA, simplefavourites, 'folders')
sourcedir = os.path.join(SMASHINGFAVOURITES, 'options')

# cleanup tempfolder if present
if os.path.isdir(tempfolder):
    shutil.rmtree(tempfolder)
    
# defaults
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
            
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

def removefile():                                   # remove
    global error, error2, DELETEFILE
    if not os.path.isfile(DELETEFILE):
        printstar()
        print 'Running deletefile'
        print ('Tried to delete %s'% DELETEFILE)
        print 'File not found'
        printstar()
    try:
        os.remove(DELETEFILE)
    except:
        pass
    if os.path.exists(DELETEFILE):
        error = ('Problem with removefile() function in %s.'% thisaddon)
        error2 = ('Could not delete the file at %s'% DELETEFILE)
        errormessage()
        
def copyfile():                         # remove
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
        
def copyfolder():
    global error, error2
    print 'running copyfolder()'
    if not os.path.isdir(SOURCE):
        error = 'Problem with copyfolder() function'
        error2 = ('SOURCE folder (%s) does not exist'% SOURCE)
        errormessage()
    if os.path.isdir(TARGET):
        # check if TARGET is an empty folder.  If it isn't generate an error
        if os.listdir(TARGET) == []:
            try:
                os.rmdir(TARGET)
            except:
                error = 'Problem with copyfolder() function'
                error2 = ('Can\'t delete TARGET folder (%s)'% TARGET)
                errormessage()
    shutil.copytree(SOURCE, TARGET)
    if not os.path.isdir(TARGET):
        error = 'Problem with copyfolder() function'
        error2 = ('Copyfolder failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()

        
def readtextfile():                                 # remove
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
    xbmc.executebuiltin('Notification(%s, has been updated)'% simplefavourites)
    exit()
	
	#########################################################################################
# let's get going
printstar()
print ('%s has started'% thisaddon)
printstar()
# check SF folders are there.
if not os.path.isdir
        
# Check tempfolder - make if necessary
if not os.path.exists(SMASHINGTEMP):
    try:
        os.mkdir(SMASHINGTEMP)
    except:
        error = ('Can\'t make folder at %s'% SMASHINGTEMP)
        errormessage()
    if not os.path.isdir(tempfolder):
        try:
            os.mkdir(tempfolder)
        except:
            error = ('Can\'t make folder at %s'% tempfolder)
            errormessage()
    else:
        try:
            shutil.rmdir(tempfolder)
            xbmc.sleep(300)
            os.mkdir(tempfolder)
        except:
            error = ('Can\'t make folder at %s'% tempfolder)
            errormessage()
# Copy all folders except all and choose to tempfolder
allcontents = []

allcontents = os.listdir(sourcedir)
allsize = len(allcontents)
c = 0
while c < allsize:
    test = allcontents[c]
    if test == 'alloptions':
        c = c + 1
        test = allcontents[c]
    if test == 'choose':
        c = c + 1
        test = allcontents[c]
    testfolder = os.path.join(sourcedir, test)
    if os.path.isdir(testfolder):
        testfile = os.path.join(testfolder, "favourites.xml")
        if os.path.isfile(testfile):
            SOURCE = testfolder
            TARGET = os.path.join(tempfolder, test)
            copyfolder()
    c = c + 1

# edit out all the 'choose more' from favourites files
listtemp = []
listtemp = os.listdir(tempfolder)
sizetemp = len(listtemp)
c = 0
while c < sizetemp:
    edit = listtemp[c]
    editfile = os.path.join(tempfolder, edit, "favourites.xml")
    f = open(editfile,"r")
    lines = f.readlines()
    f.close()
    f = open(editfile,"w")
    for line in lines:
        if 'Choose More' not in line:
            f.write(line)
    f.close()
    c = c + 1
    
# Move folders into simple favourites
# cleanup tempfolder if present
if os.path.isdir(simpledir):
    shutil.rmtree(simpledir)
    xbmc.sleep(300)
    if os.path.isdir(simpledir):
        error = ('Could not delete %s'% simpledir)
        errormessage()
os.mkdir(simpledir)
c = 0
while c < sizetemp:
    foldername = listtemp[c]
    SOURCE = os.path.join(tempfolder, foldername)
    TARGET = os.path.join(simpledir, foldername)
    copyfolder()
    c = c + 1


finish()


        ####################################################################################
        




# drink beer, eat pies 
