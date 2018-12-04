# -*- coding: utf-8 -*-
# This does nothing, just lists sources, functions to use in other scripts

# import
import xbmc
import xbmcgui
import os
import shutil
import sys
import socket

#hacks!
# if looping through too many times:
sys.setrecursionlimit(10000)

# Run this first, so can define in terms of thisaddon:
def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)




# get info
host = socket.gethostname()

# sources
# path to kodi addons folders:	
ADDONSPATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
DEFAULTADDONSPATH = os.path.join(xbmc.translatePath('special://xbmc/'), "addons")

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISC, "addons")
OLDADDONS = os.path.join(SMASHINGADDONS, "oldaddons")




# paths to add that depend on 'thisaddon':
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "%sisrunning.txt"% thisaddon)




# default messages
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
error3 = 'none'
errornotification = 'none'
message = 'none'       # set default to 'none'; only print if changed




#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# errors
def errormessage():
    global error, error2, errornotification
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    if error in globals():
        if not error == 'none':
            print error
    if error2 in globals():
        if not error2 == 'none':
            print error2
    if error3 in globals():
        if not error3 == 'none':
            print error3
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    # try marker stuff
    if MARKER in globals():
        if os.path.exists(MARKER):
            try:
                os.remove(MARKER)
                if not os.path.exists(MARKER):
                    xbmc.sleep(300)
            except:
                print ('The marker file (%s) could not be deleted'% MARKER)
                xbmc.sleep(3000)
                xbmc.executebuiltin('Notification(Marker file - was not removed)')
    if errornotification in globals():
        if not errornotification == 'none':
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(errornotification)')
    printstar()
    exit()    
    
    
# remove a folder recursively
def removedeletefolder():
    global error, error2, errornotification
    print 'running removedeletefolder()'
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
        error = ('Problem with removedeletefolder() function in %s.'% thisaddon)
        error2 = ('Could not delete the folder at %s'% DELETEFOLDER)
        printstar()
        errornotification = ('Something went wrong, Could not delete %s'% DELETEFOLDER)
        errormessage()
    else:
        printstar()
        print ('%s has deleted %s'% (thisaddon, DELETEFOLDER))
        printstar()
        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFOLDER)
    xbmc.sleep(300)




