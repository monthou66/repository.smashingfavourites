#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import os
import shutil

# sources
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
leiafavsfolder = os.path.join(SMASHINGFAVOURITES, "leiafavourites")
leiadefaultfavs = os.path.join(SMASHINGFAVOURITES, "leiafavourites", "default", "favourites.xml")
leiaalternatefavs = os.path.join(SMASHINGFAVOURITES, "leiafavourites", "alternate", "favourites.xml")
leiarealfavs = os.path.join(USERDATA, "favourites.xml")

# defaults
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
argument = 'updatereal'
refresh = 'false'               # if refresh = true favourites will be reloaded

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

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
    global argument, SOURCE, TARGET, refresh
    size = len(sys.argv)
    if len(sys.argv) > 1:
        argument = sys.argv(1)
    if argument == 'updatereal':
        SOURCE = leiadefaultfavs
        TARGET = leiarealfavs
#        TARGET = USERDATA
        refresh = 'true'
    elif argument == 'updatealternate':
        SOURCE = leiaalternatefavs
        TARGET = leiarealfavs
        refresh = 'true'
    elif argument == 'updatesmashing':
        SOURCE = leiarealfavs
        TARGET = leiadefaultfavs
        
####################################################################################################
##      Arguments
##      updatereal = copy from default leia folder to userdata (and refresh favourites)
##      updatesmashing = copy from userdata to smashingfavourites/leiafavourites/default
##      updatealternate = copy from alternate leia folder to userdata (and refresh favourites)
##
####################################################################################################

def removefile():
    global error, error2, DELETEFILE
    if not os.path.isfile(DELETEFILE):
        printstar()
        print 'Running deletefile'
        print ('Tried to delete %s'% DELETEFILE)
        print 'File not found'
        printstar()
    if os.path.isfile(DELETEFILE):
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
        xbmc.sleep(300)
        shutil.copyfile(SOURCE, TARGET)
        xbmc.sleep(300)
    except:
        error = 'Problem with copyfile() function'
        error2 = ('Copyfile failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
        
def refreshfavs():
    xbmc.executebuiltin("System.LogOff")
    xbmc.sleep(300)
    xbmc.executebuiltin("LoadProfile(Master user)")

def finish():
    printstar()
    print ('%s is shutting down'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Favourites updated, all done)')
    exit()

######################################################################################################
# get started

thisaddon = sys.argv[0]
getoptions()
printstar()
print ('%s has started'% thisaddon)
print ('argument is %s' % argument)
print ('SOURCE = %s'% SOURCE)
print ('TARGET = %s'% TARGET)
print ('refresh = %s'% refresh)
printstar()

# check source exists - error out if not
if not os.path.isfile(SOURCE):
    error = ('SOURCE file not found - %s'% SOURCE)
# get rid of target file
DELETEFILE = TARGET
removefile()
# copy file across
copyfile()
# refresh favs if needed
if refresh == 'true':
    refreshfavs()

finish()


# drink beer, eat pies 