# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os
import shutil
import socket


# define some places
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
# path to advancedsettings options folders:	
FOLDERSPATH = os.path.join(SMASHINGFAVOURITES, "advancedsettings")
# path to working advancedsettings.xml
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")


# hacky hacks
PLATFORM = 'Noclue'
currentadvancedsettings = 'Absolutelynoidea'
debugcurrent = 'nobloomingclue'
ADVSETTS = []

TEMPLATESFOLDER = os.path.join(FOLDERSPATH, "templates")
TEMPLATE = os.path.join(TEMPLATESFOLDER, "template.xml")
#settingsfile = 

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"  

def error():
    printstar()
    print ('Error running %s'% thisaddon)
    if not errormessage == 'none':
        print 'Reported error is:'
        print errormessage
    printstar()        
    xbmc.executebuiltin('Notification(Problem with %s, Check the log for details)'% thisaddon)
    exit()

def postmessage():
    global message, message1, message2
    if not message == 'none':
        printstar()
        print ('%s message:'% thisaddon)
        print message
        if not message1 == 'none':
            print message1
            if not message2 == 'none':
                print message2
        printstar()        
    message = 'none'
    message1 = 'none'
    message2 = 'none'

def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
#    a = sys.argv[1]
    printstar()
    print ('%s has started'% thisaddon)
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
    getos()
	
# Get os
def getos():
    global PLATFORM, message, message1, host
    host = socket.gethostname()
    if xbmc.getCondVisibility('system.platform.android'):
        PLATFORM = 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        PLATFORM = 'linux'
        if xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
            PLATFORM = 'libreelec'
        else:
            errormessage = 'Platform identifies as linux but not as libreelec.'
            error()
            
    elif xbmc.getCondVisibility('system.platform.windows'):
        PLATFORM = 'windows'
    else:
        errormessage = 'Unable to identify the system platform.'
        error()
    # log results:
    message = ('Hostname is %s' % host)
    message1 = ('You\'re using %s' % PLATFORM)
    postmessage()

def getoptions():
# select machine drives are on

# select which drives are being used

# select local or mysql library

# if mysql what machine is it on?

# select loglevel

# select cache option (zero or not)







# Drink beer