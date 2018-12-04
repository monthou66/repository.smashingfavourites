# -*- coding: utf-8 -*-
# try restore
# switch estuary, unload skin, delete settings.xml, copy in settings.xml, reload skin, check???
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

# Get running skin
SKIN = xbmc.getSkinDir()
if SKIN == "skin.xonfluence":
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.estuary"}}')
    xbmc.executebuiltin('SendClick(11)')
xbmc.executebuiltin('UnloadSkin()')
	
SKINFOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data", "skin.xonfluence")
BACKUPFOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashing", "smashingfavourites", "backups", "skins", "xonfluence")
XONFOPTION = os.path.join(BACKUPFOLDER, "xonfoption.txt")
SETTINGS = os.path.join(SKINFOLDER, "settings.xml")

# Test
printstar()
print ("SKINFOLDER is %s" % SKINFOLDER)
print ("BACKUPFOLDER is %s" % BACKUPFOLDER)
print ("XONFOPTION is %s" % XONFOPTION)
print ("SETTINGS is %s" % SETTINGS)
printstar()

if os.path.exists(XONFOPTION):
    f = open(XONFOPTION)
    g = (f.read())
    OPTION = g	
    h = len(OPTION)
    f.close()		
    if h > 0:
        CHECK = os.path.join(BACKUPFOLDER, "%s.txt" % OPTION)
        if os.path.exists(CHECK):
            os.remove(CHECK)
        else:
            OPTION = 'none'
    else:
        OPTION = 'none'
else:
    OPTION = 'none'
		
print ("OPTION is %s" % OPTION)
	
if os.path.exists(XONFOPTION):
    os.remove(XONFOPTION)
		
if os.path.exists(SETTINGS):		
    os.remove(SETTINGS)

if OPTION != 'none':	
    SAVE = os.path.join(BACKUPFOLDER, "backups", OPTION, "settings.xml")
    printstar()    
    print ("SAVE is %s" % SAVE)
    shutil.copy(SAVE, SKINFOLDER)
    printstar()
    SAVEFOLDER = os.path.join(BACKUPFOLDER, "backups", OPTION)
    SAVEXONFOPTION = os.path.join(SAVEFOLDER, "xonfoption.txt")
    print ("SAVEXONFOPTION is %s" % SAVEXONFOPTION)
    SAVEOPTION = os.path.join(SAVEFOLDER, "%s.txt" % OPTION)	
    print ("SAVEOPTION is %s" % SAVEOPTION)
    shutil.copy(SAVEXONFOPTION, BACKUPFOLDER)
    shutil.copy(SAVEOPTION, BACKUPFOLDER)
    print "Skin restored, yay"
    SKIN = xbmc.getSkinDir()
    if SKIN != "skin.xonfluence":
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.xonfluence"}}')
        xbmc.executebuiltin('SendClick(11)')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skincolors","value":"gray.xml"}}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skintheme","value":"gray"}}')
    xbmcgui.Dialog().ok(OPTION, '                                                has been restored')
else:
    print "No way Jose"
    xbmc.executebuiltin('ReloadSkin()')
    xbmcgui.Dialog().ok('Tough', 'luck buddy')
exit()