# -*- coding: utf-8 -*-
# clonepvr.iptvsimple.py
# This clones pvr.iptvsimple automatically when it updates.

import xbmc
import os
import shutil


# define file locations
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
PVRIPTVSIMPLE = os.path.join(ADDONS, "pvr.iptvsimple")
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/pvr.iptvsimple'))
CLONEADDON = os.path.join(ADDONS, "pvr.iptvsimplefab")
XML = os.path.join(CLONEADDON, "addon.xml")
XMLIN = os.path.join(CLONEADDON, "addon.xml.in")
DLLOLD = os.path.join(CLONEADDON, "pvr.iptvsimple.dll")
DLLNEW = os.path.join(CLONEADDON, "pvr.iptvsimplefab.dll")
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISC, "addons")
OLDADDONS = os.path.join(SMASHINGADDONS, "oldaddons")
OLDCLONE = os.path.join(OLDADDONS, "pvr.iptvsimplefab")
OLDCLONEDLL = os.path.join(OLDCLONE, "pvr.iptvsimplefab.dll")
MARKERSOURCE = os.path.join(OLDADDONS, "cloned.txt")
CLONESCRIPT = os.path.join(SMASHINGFAVOURITES, "scripts", "utilityscripts", "clonepvriptvsimple.py")
OLDDLLSTODELETE = os.path.join(OLDADDONS, "temp", "iptvsimplefabdlls")
error = 'non-specific'
#print ('SMASHINGFAVOURITES is %s'% SMASHING)
#print ('MISC is %s'% MISC)
#print ('SMASHINGADDONS is %s'% SMASHINGADDONS)
#print ('OLDCLONE is %s'% OLDCLONE)

#xbmc.executebuiltin('StopScript(CLONESCRIPT)')

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
    exit()

def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

#def getarguments():
#    global



def removeolddlls():
    if not os.path.exists(OLDDLLSTODELETE):
        os.makedirs(OLDDLLSTODELETE)
    c = 1
    while c < 20:
        
        num = str(c)
        OLDCLONEFOLDER = os.path.join(OLDDLLSTODELETE, num)
        if os.path.exists(OLDCLONEFOLDER):
            try:
                os.remove(OLDCLONEFOLDER)
                if not os.path.exists(OLDCLONEFOLDER):
                    print ('%s folder has been deleted'% OLDCLONEFOLDER)
                else:
                    print ('Failed to delete %s folder'% OLDCLONEFOLDER)
            except:
                print ('Failed to delete %s folder'% OLDCLONEFOLDER)
        else:
            print ('No folder found at %s'% OLDCLONEFOLDER)
        c = c + 1

        
def identifytempfolder():
    global FOLDER
#    temp = 1
    c = 1
    while c < 20:
        temp = str(c)
        FOLDER = os.path.join(OLDDLLSTODELETE, temp)
        if os.path.exists(FOLDER):
#            temp = temp + 1
            c = c + 1
        else:
            c = 20
    print ('temp folder is %s'% FOLDER)
    
def deleteoldclone():
    global FOLDER, error
    if os.path.exists(OLDCLONE):
        try:
            shutil.rmtree(OLDCLONE)
        except:
            if os.path.exists(OLDCLONEDLL):
                if not os.path.exists(FOLDER):
                    os.makedirs(FOLDER)
                    MOVED = os.path.join(FOLDER, "pvr.iptvsimplefab.dll")
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

def deletetempfolder():
    if os.path.exists(OLDDLLSTODELETE):
        try:
            shutil.rmtree(OLDDLLSTODELETE)
            print ('%s folder deleted'% OLDDLLSTODELETE)
        except:
            print ('%s folder could not be deleted.'% OLDDLLSTODELETE)


startaddon()
removeolddlls()    
identifytempfolder()
deleteoldclone()    
deletetempfolder()    
exit()

# Drink beer



