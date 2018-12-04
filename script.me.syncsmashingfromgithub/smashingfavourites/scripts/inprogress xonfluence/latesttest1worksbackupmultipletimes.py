# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil
# To show up in log:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def printworking():
    print "smashingxonf is doing stuff."
	
def printproblem():
    print "There is a problem with smashingxonfluence."
	
def printabandon():
    print "Script ended by user."
	
def printnorestore():
    print "No restore performed."
	
def printnobackup():
    print "No backup performed."
	
def printbackup():
    print "Xonfluence has been backed up."
	
def backupdone():
    xbmc.executebuiltin('Notification(Xonfluence has been, backed up)')
	
XONFOPTION = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/xonfoption.txt")
SETTINGS = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/settings.xml")

def makeoptionstuff():
    keyboard = xbmc.Keyboard("", "Enter backup name", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
	    global  OPTION
            OPTION = keyboard.getText()
#        if xbmcgui.Dialog().yesno("Backup Xonfluence","to %s","Confirm?" % OPTION):
#        if xbmcgui.Dialog().yesno("Backup Xonfluence now?"):
            yesnowindow = xbmcgui.Dialog().yesno("Backup Xonfluence","Click yes to start","Click No to get a raspberry")
            if not yesnowindow:
                xbmc.executebuiltin('Notification(You have earned, a raspberry)')
                exit()
            else:		
                make = open(XONFOPTION, 'w')
                make.write("%s" % OPTION)
                global CHECK
                CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/%s.txt" % OPTION)
                produce = open(CHECK, 'w')
                produce.close()
                FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/backups/%s" % OPTION)
                if not os.path.exists(FOLDER):
                    os.makedirs(FOLDER)
    else:
        exit()
		
def backupxonf():
    FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/backups/%s" % OPTION)
    shutil.copy(XONFOPTION, FOLDER)
    shutil.copy(CHECK, FOLDER)    
    shutil.copy(SETTINGS, FOLDER)
	
def addtofavourites():
# add entry to favourites
# identify xonfluence favourites file - take code from smashingfavourites.py
# read current favourite
    FAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile'), "favourites.xml")
# get line 2
    line = open(FAVOURITESFILE).readlines()[1]
# find xonfluence favourites
    CURRENT = line[line.find("/icons/")+7:line.find(".png")]
    if CURRENT != 'xonfluence':
        NEWFAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/xonfluence/favourites.xml")
        if not os.path.isfile(NEWFAVOURITESFILE):
            exit()
# Move favourites files if necessary - code from smashingfavourites.py
        else:
            OLDFAVOURITES = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/", CURRENT)
            OLDFAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/", CURRENT, "favourites.xml")            
            os.rename(FAVOURITESFILE, OLDFAVOURITESFILE)
            os.rename(NEWFAVOURITESFILE, FAVOURITESFILE)		
# add the new favourite
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title":"Restore %s", "type":"script", "path":"special://masterprofile/smashing/smashingfavourites/scripts/skinscripts/smashingxonfluence.py, restore, %s", "thumbnail":""}, "id": 1}' % (OPTION, OPTION))
# clean &quot;
    infile = os.path.join(xbmc.translatePath('special://userdata/favourites.xml'))
    outfile = os.path.join(xbmc.translatePath('special://userdata/1favourites.xml'))
    delete_start = ["RunScript(&quot;"]
    delete_end = ["%s&quot;" % OPTION]
    fin = open(infile)
    fout = open(outfile, "w+")
    for line in fin:
        for word in delete_start:
            line = line.replace(word, "RunScript(")
        for word in delete_end:
            line = line.replace(word, "%s" % OPTION)	
        fout.write(line)
    fin.close()
    fout.close()
    os.remove(infile)
    os.rename(outfile, infile)	

#check if backup exists
if os.path.exists(XONFOPTION):
    f = open(XONFOPTION)
    OPTION = (f.read())		
    h = len(OPTION)
    f.close()
# checking current backup name
    printstar()
    printworking()
    print ("The current backup is %s" % OPTION)
# remove backup pointers if no backup exists	
    if h > 0:
        CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/%s.txt" % OPTION)
        if not os.path.exists(CHECK):
            os.remove(XONFOPTION)
            makeoptionstuff()
        else:
# option to redo backup or make new one
            yesnowindow = xbmcgui.Dialog().yesno("You already have a backup called %s","Click yes to save changes and redo this backup","Click No to make a new backup")
            if yesnowindow:
                SAVEDSETTINGS = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/backups", OPTION, "settings.xml")
                FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/backups/%s" % OPTION)
                os.remove(SAVEDSETTINGS)
                shutil.copy(SETTINGS, FOLDER)
                printstar()
                printworking()
                printbackup()
                printstar()
                backupdone()				
                exit()
            else:		
                os.remove(XONFOPTION)
                os.remove(CHECK)
                makeoptionstuff()
else:
    makeoptionstuff()
    
backupxonf()
addtofavourites()
printstar()
print 'Done!'
printstar()
exit()	
