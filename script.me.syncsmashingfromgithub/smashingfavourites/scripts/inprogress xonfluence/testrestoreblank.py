# -*- coding: utf-8 -*-
#testrestoreblank.py

import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil

# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SKINBACKUPS = os.path.join(SMASHINGFAVOURITES, "backups", "skins")
skinpath = xbmc.translatePath('special://skin')


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
		
def restore():

    SWITCH = 'skin.estuary'	
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% SWITCH)
    xbmc.executebuiltin('SendClick(11)')
    xbmc.executebuiltin('UnloadSkin()')
    print 'checkpoint1'
#    FILE = os.path.join(SMASHINGFAVOURITES, "backups", "skins", "skin.xonfluence", "real", "settings.xml")
    FILE = os.path.join(SMASHINGFAVOURITES, "backups", "skins", "skin.xonfluence", "blank", "settings.xml")
    datafolder = os.path.join(USERDATA, "addon_data", "skin.xonfluence")
    TARGET = os.path.join(datafolder, "settings.xml")
    print 'checkpoint2'
    print ('FILE is %s'% FILE)
    print ('TARGET is %s'% TARGET)
    if os.path.exists(TARGET):
        os.remove(TARGET)
        xbmc.sleep(1000)
    shutil.copyfile(FILE, TARGET)
#    shutil.copy(FILE, datafolder)
    print 'checkpoint3'
#    xbmc.executebuiltin('ReloadSkin()')
#    print 'checkpoint4'
#    exit()
    skin = 'skin.xonfluence'
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% skin)        
    xbmc.executebuiltin('SendClick(11)')
    newtheme = 'gray'
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skintheme","value":"%s"}}'% newtheme)
    newskincolour = 'gray'
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skincolors","value":"%s"}}'% newskincolour)

	


startaddon()
restore()
print 'checkpoint4'
exit()


	

