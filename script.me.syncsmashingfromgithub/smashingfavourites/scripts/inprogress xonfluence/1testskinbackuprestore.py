# -*- coding: utf-8 -*-
#testskinbackuprestore.py

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

def error():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Check, %s)'% thisaddon)
    exit()
	
def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

def restoredone():
    printstar()
    print ('%s has been restored from %s.'% (SKIN, CHOICE))
    printstar()
    xbmc.executebuiltin('Notification(%s has been, restored from %s)'% (SKIN, CHOICE))
	
def backupdone():
    printstar()
    print ('%s has been backed up.'% SKIN)
    printstar()
    xbmc.executebuiltin('Notification(%s has been, backed up)'% SKIN)
	
def getcurrent():
    # get current active skin, plus theme and colour theme.
    # set backup folder and addon_data folder
    # alternative:
    # skin = xbmc.getSkinDir()
    global skin, theme, skincolour, font, backupfolder, datafolder, SETTINGS, OLDSETTINGS, OLDTHEME
    skin = os.path.basename(os.path.normpath(skinpath))
    theme = xbmc.getInfoLabel('Skin.CurrentTheme')
    skincolour = xbmc.getInfoLabel('Skin.CurrentColourTheme')
    font = xbmc.getInfoLabel('Skin.Font')
    backupfolder = os.path.join(SKINBACKUPS, skin)
    datafolder = os.path.join(USERDATA, "addon_data", skin)
    SETTINGS = os.path.join(datafolder, "settings.xml")
    OLDSETTINGS = os.path.join(datafolder, "oldsettings.xml")
    OLDTHEME = os.path.join(datafolder, 'themebackup.txt')
	# check backup folder exists - make it if not
    if not os.path.exists(backupfolder):
        os.mkdir(backupfolder)
    printstar()
    print ('The current skin id is %s'% skin)
    print ('The current theme is %s'% theme)
    print ('The current skin colour theme is %s'% skincolour)
    printstar()

def listfolders():
    # list existing backup folders
    global backups, howmany
    print 'check1'
    LIST = []
    LIST = os.listdir(backupfolder)
    number = len(LIST)
    backups = []
    c = 0
    while c < number:
        check = LIST[c]
        checkpath = os.path.join(backupfolder, check)
        if os.path.isdir(checkpath):
            backups.append(check)
        c = c + 1
    howmany = len(backups)
    print 'check2'		
	
def chooseoption():
    # backup or restore
    # view backups, backup existing, backup new, restore, restore last, delete backup, rename backup
    global OPTION, text, backups, last, OLDSETTINGS
    OPTIONSLIST = ['Restore skin settings from backup', 'Backup skin settings', 'Rename backups', 'Delete Backups', 'Quit']
    back = 'Go back to options list'
    OPTION = xbmcgui.Dialog().select("Options", OPTIONSLIST)
    print 'check3'
    if OPTION == 0:
        if howmany >= 1:
            text = 'Choose the backup to restore'
        else:
            text = 'There are no existing backups'
        if os.path.isfile(OLDSETTINGS):
            last = 'Restore previous settings'
            backups.append(last)
        print 'check4'
    elif OPTION == 1:
        text = 'Choose where you want to back up.'
        last = 'Make a new backup'
        backups.append(last)
    elif OPTION == 2:
        text = 'Choose the backup to rename'
    elif OPTION == 3:
        text = 'Choose the backup to delete'
    elif OPTION	 == 4:
        xbmc.executebuiltin('Notification(%s, is stopping)'% thisaddon)
        exit()
    else:
        xbmc.executebuiltin('Notification(No option selected, %s is stopping)'% thisaddon)
        exit()	
	
def choosefromlist():
    global FOLDER, FILE, THEME
    printstar()
    print ('backups are %s'% backups)
    back = 'Go back to options list'
    backups.append(back)
    quit = 'Quit'
    backups.append(quit)
    print ('now backups are %s'% backups)
    printstar()
    length = len(backups)
    CHOOSE = xbmcgui.Dialog().select(text, backups)	
    if not 0 <= CHOOSE <= length:
        xbmc.executebuiltin('Notification(No option selected, %s is stopping)'% thisaddon)
        exit()
    if backups[CHOOSE] == quit:
        xbmc.executebuiltin('Notification(%s, is stopping)'% thisaddon)
        exit()
    if backups[CHOOSE] == back:
        chooseoption()
    if backups[CHOOSE] == 'Restore previous settings':
        FOLDER = datafolder
        FILE = OLDSETTINGS
    else:
        FOLDER = backups[CHOOSE]
        FILE = os.path.join(backupfolder, FOLDER, "settings.xml")
    THEME = os.path.join(FOLDER, 'themebackup.txt')
		
def restore():
    global theme, skincolour, font, FILE, OLDSETTINGS, THEME
    # switch into another skin
    if not skin == 'skin.estuary':
        SWITCH = 'skin.estuary'
        print 'check5'
    else:
        if xbmc.getCondVisibility('System.HasAddon(skin.estouchy)'):
            SWITCH = 'skin.estouchy'
        elif xbmc.getCondVisibility('System.HasAddon(skin.confluence)'):
            SWITCH = 'skin.confluence'
        else:
            printstar()
            print ('No skin available to switch into. %s has stopped'% thisaddon)
            printstar()
            error()
    print 'check6'
	
# test
#    xbmc.executebuiltin('UnloadSkin()')
#    xbmc.sleep(300)	
	
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% SWITCH)
    xbmc.executebuiltin('SendClick(11)')
    print 'check7'
    xbmc.executebuiltin('UnloadSkin()')


    print 'check8'
    # back up existing settings inside skin's addon_data folder
    # if restoring previous settings from addon_data rename backed up files first
    if FILE == OLDSETTINGS:
        print 'check9'
        TEMPFILE = os.path.join(FOLDER, 'tempsettings.xml')
        if os.path.exists(TEMPFILE):
            os.remove(TEMPFILE)
            xbmc.sleep(300)
        os.rename(FILE, TEMPFILE)
        FILE = TEMPFILE
        print 'check10'
        if os.path.isfile(THEME):
            TEMPTHEME = os.path.join(FOLDER, 'tempthemebackup.txt')
            os.rename(THEME, TEMPTHEME)
            THEME = TEMPTHEME
            print 'check11'
    # remove existing backup from addon_data folder	
    if os.path.isfile(OLDSETTINGS):
        os.remove(OLDSETTINGS)
        print 'check12'
    if os.path.isfile(OLDTHEME):
        os.remove(OLDTHEME)
        print 'check13'
    # save existing settings:
    os.rename(SETTINGS, OLDSETTINGS)
    f = open(OLDTHEME, 'w')
    f.write('This file has the Theme, Colours and Font associated with the backup of %s\n'% skin)
    f.write('Theme:\n')
    f.write('%s\n'% theme)
    f.write('Skincolours:\n')
    f.write('%s\n'% skincolour)
    f.write('Font:\n')
    f.write('%s\n'% font)
    f.close()
    print 'check14'
    # restore settings
# test
    CURRENT = xbmc.getSkinDir()
    printstar()
    print ('FILE is %s'% FILE)
    print ('SETTINGS are %s'% SETTINGS)
    print ('Current skin is %s'% CURRENT)
    print ('datafolder is %s'% datafolder)
    printstar()
# shutil.copy - need to specify destination folder, not file!!!
#    shutil.copy(FILE, SETTINGS)
#    print 'checkpoint1'
#    shutil.copy(FILE, datafolder)
#    print 'checkpoint2'
    TARGET = os.path.join(datafolder, "settings.xml")
    print ('FILE is %s'% FILE)
    print ('TARGET is %s'% TARGET)
    if os.path.exists(TARGET):
        os.remove(TARGET)
        xbmc.sleep(1000)
				
# test		
    if os.path.exists(TARGET):
        print 'bollocks'
    if not os.path.exists(TARGET):
        print 'rowlocks'
		
		
#    shutil.copyfile(FILE, TARGET)

# test
    xbmc.sleep(1000)
#    xbmc.executebuiltin('ReloadSkin()')
#    exit()
#test
    TEST = os.path.join(datafolder, "test.xml")	
    shutil.copyfile(FILE, TEST)
    xbmc.sleep(300)
    if os.path.exists(TARGET):
        os.remove(TARGET)
        xbmc.sleep(300)
    os.rename(TEST, TARGET)

	
    newtheme = theme
    newskincolour = skincolour
    newfont = font
    print 'check15'
    mylist = []
    if os.path.exists(THEME):
        with open(THEME) as f:
            mylist = f.read().splitlines()
            length = len(mylist)
        if len(mylist) == 7:
            newtheme = mylist[2]
            newskincolour = mylist[4]
            newfont = mylist[6]
    # restart skin
    print 'check16'
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% skin)        
    xbmc.executebuiltin('SendClick(11)')
    print 'check17'
    # set theme and colours if necessary	
    theme = xbmc.getInfoLabel('Skin.CurrentTheme')
    skincolour = xbmc.getInfoLabel('Skin.CurrentColourTheme')
    font = xbmc.getInfoLabel('Skin.Font')
    if not newtheme ==  theme:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skintheme","value":"%s"}}'% newtheme)
        print 'check18'
    print 'check19'
    if not newskincolour == skincolour:
        print ('newskincolour is %s'% newskincolour)
        print ('skincolour is %s'% skincolour)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skincolors","value":"%s"}}'% newskincolour)
        print 'check20'
    print 'check21'
    if not newfont == font:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.font","value":"%s"}}'% newfont)		
        print 'check22'
    print 'check23'
    exit()
	
#def backup():



#def rename():


#def delete():
	
# test
def test1():
    global SKIN, CHOICE
    SKIN = 'xonfluence'
    CHOICE = 'test'
    backupdone()
    xbmc.sleep(5000)
    restoredone()
    exit()
# test1()		
def test2():
    startaddon()
    getcurrent()
    chooseoption()
    exit()	
#test2()
def test3():
    startaddon()
    getcurrent()
    listfolders()
    chooseoption()
    choosefromlist()
    exit()
#test3()

def test4():
    startaddon()
    getcurrent()
    listfolders()
    chooseoption()
    choosefromlist()
    if OPTION == 0:
        restore()
    exit()
test4()

	

