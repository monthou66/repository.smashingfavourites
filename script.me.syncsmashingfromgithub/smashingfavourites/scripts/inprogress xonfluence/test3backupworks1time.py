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
	
XONFOPTION = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/xonfoption.txt")
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
                make.close()
                global CHECK
                CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s .txt" % OPTION)
                produce = open(CHECK, 'w')
                produce.close()
                FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s" % OPTION)
                if not os.path.exists(FOLDER):
                    os.makedirs(FOLDER)
    else:
        exit()
		
def backupxonf():
    FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s" % OPTION)
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
        FAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/xonfluence/favourites.xml")
        if not os.path.isfile(FAVOURITESFILE):
            exit()
# add
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
    g = (f.read())		
    h = len(g)
    f.close()
    if h > 0:
        OPTION = g
        CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s .txt" % OPTION)
        if not os.path.exists(CHECK):
            os.remove(XONFOPTION)
            makeoptionstuff()
        else:
            os.remove(XONFOPTION)
            makeoptionstuff()
else:
    makeoptionstuff()
    backupxonf()
    addtofavourites()
    printstar()
    print 'Done!'
    printstar()
    exit()	
