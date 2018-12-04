# -*- coding: utf-8 -*-
# editxonf.py
# Simple addon - edits skin files when prompted
import xbmc
import xbmcgui
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "editxonf.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(editxonf.py, started)')

# define file locations
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
XONF = os.path.join(ADDONS, "skin.xonfluence")
XMLFOLDER = os.path.join(XONF, "720p")
WORKINGFOLDER = os.path.join(XONF, "temp")
MARKER = os.path.join(XMLFOLDER, "a.default.Includes.xml")

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
NEWFILES = os.path.join(MISC, "addons", "edits", "skin.xonfluence")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
BACKUPS = os.path.join(SMASHINGTEMP, "backups")
XONFCOPY = os.path.join(BACKUPS, "skin.xonfluence")


def copyfile():
    print 'running copyfile()'
    try:
        shutil.copyfile(SOURCE, TARGET)
    except:
        printstar()
        print 'Problem with xonfedit.py'
        print 'Could not copy file'
        print ('SOURCE = %s'% SOURCE)
        if os.path.exists(SOURCE):
            print 'SOURCE is valid'
        else:
            print 'SOURCE is not valid'
        print ('TARGET = %s'% TARGET)
        printstar()
        xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
        exit()

def movefile():
    print 'running movefile():'
    if os.path.exists(TARGET):
        try:
            os.remove(TARGET)
            xbmc.sleep(300)
        except:
            printstar()
            print 'Problem with xonfedit.py'
            print 'Could not delete file'
            print 'Make sure any incomplete skin edits are removed'
            print ('Problem file = %s'% TARGET)
            printstar()
            xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
            exit()
    try:
        os.rename(SOURCE, TARGET)
    except:
        printstar()
        print 'Problem with xonfedit.py'
        print 'Could not move file'
        print 'Make sure any incomplete skin edits are removed'
        print ('SOURCE = %s'% SOURCE)
        print ('TARGET = %s'% TARGET)
        printstar()
        xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
        exit()
        
def replacetext():
    print 'running replacetext()'
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(old, new)) 
        
# check if xonfluence is installed - if not quit
if not xbmc.getCondVisibility('System.HasAddon(skin.xonfluence)'):
    printstar()
    print 'Problem with xonfedit.py'
    print 'xonfluence is not installed'
    print 'Stopping xonfedit.py'
    printstar()
    xbmc.executebuiltin('Notification(skin.xonfluence, is not installed)')
    exit()
# check if marker is present - if so edits are not needed, so quit
if os.path.isfile(MARKER):
    printstar()
    print ('Marker file is present at %s'% MARKER)
    print 'No need to redo edits'
    print 'Stopping xonfedit.py'
    printstar()
    xbmc.executebuiltin('Notification(skin.xonfluence does not need, to be updated)')
    exit()

# If we're still here it looks like we need to update:
# Make a copy of the current skin folder, so we can roll back if necessary
# first check for existing backup, delete if necessary
if not os.path.exists(SMASHINGTEMP):
    os.mkdir(SMASHINGTEMP)
    xbmc.sleep(300)
if not os.path.exists(BACKUPS):
    os.mkdir(BACKUPS)
    xbmc.sleep(300)
if os.path.exists(XONFCOPY):
    yesnowindow = xbmcgui.Dialog().yesno('Existing xonfluence backup will be overwritten', "", "                                  Click Yes to proceed")
    if not yesnowindow:
        printstar()
        print 'Script cancelled by user'
        printstar()
        exit()
    else:        
        try:
            shutil.rmtree(XONFCOPY)
            xbmc.sleep(300)
        except:
            printstar()
            print 'Problem with xonfedit.py'
            print 'Could not delete backup folder'
            print 'Make sure any incomplete skin edits are removed'
            print ('Problem folder = %s'% XONFCOPY)
            printstar()
            xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
            exit()
# copy skin to backup folder
shutil.copytree(XONF, XONFCOPY)
xbmc.sleep(300)
xbmc.executebuiltin('Notification(Xonfluence, has been backed up)')

# Delete working folder if present:
if os.path.exists(WORKINGFOLDER):
    c = 0
    while c < 50:
        try:
            shutil.rmtree(WORKINGFOLDER)
        except:
            xbmc.sleep(300)
            print ('Could not delete WORKINGFOLDER at %s'% WORKINGFOLDER)
            print ('c = %d'% c)
        if not os.path.exists(WORKINGFOLDER):
            c = c + 50
            xbmc.sleep(300)
        else:
            c = c + 1
    if os.path.exists(WORKINGFOLDER):
        printstar()
        print 'Problem with xonfedit.py'
        print 'Could not delete WORKINGFOLDER'
        print 'Stopping xonfedit.py'
        printstar()
        xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
        exit()
# Make working folder:
os.mkdir(WORKINGFOLDER)
# copy files into working folder:
SOURCE = os.path.join(XMLFOLDER, "Includes.xml")
TARGET = os.path.join(WORKINGFOLDER, "Includes.xml")
copyfile()
SOURCE = os.path.join(XMLFOLDER, "IncludesBackgroundBuilding.xml")
TARGET = os.path.join(WORKINGFOLDER, "IncludesBackgroundBuilding.xml")
copyfile()
SOURCE = os.path.join(XMLFOLDER, "MyVideoNav.xml")
TARGET = os.path.join(WORKINGFOLDER, "MyVideoNav.xml")
copyfile()

# edit Includes.xml            
file = os.path.join(WORKINGFOLDER, "Includes.xml")
old = '	<include file="ViewsWeather.xml" />'
new = '	<include file="ViewsWeather.xml" />\n	<include file="ViewMediaInfoSets.xml" />   <!-- added this line -->'
replacetext()

# edit IncludesBackgroundBuilding.xml
file = os.path.join(WORKINGFOLDER, "IncludesBackgroundBuilding.xml")
old = 'Control.IsVisible(512)</visible>'
new = 'Control.IsVisible(512) | Control.IsVisible(525)</visible>   <!-- added 525 -->'
replacetext()

# edit MyVideoNav.xml
file = os.path.join(WORKINGFOLDER, "MyVideoNav.xml")
old = '</views>'
new = ',525</views>                <!-- added 525 -->'
replacetext()
old = '<!-- view id = 50 -->'
new = '<!-- view id = 50 -->\n			<include>MediaInfoSets</include>   <!-- added this line -->\n			<!-- view id = 525 -->   <!-- added this line -->'
replacetext()

# rename files in 720p folder, move new files in
SOURCE = os.path.join(XMLFOLDER, "Includes.xml")
TARGET = os.path.join(XMLFOLDER, "a.default.Includes.xml")
movefile()
SOURCE = os.path.join(XMLFOLDER, "IncludesBackgroundBuilding.xml")
TARGET = os.path.join(XMLFOLDER, "a.default.IncludesBackgroundBuilding.xml")
movefile()
SOURCE = os.path.join(XMLFOLDER, "MyVideoNav.xml")
TARGET = os.path.join(XMLFOLDER, "a.default.MyVideoNav.xml")
movefile()
SOURCE = os.path.join(WORKINGFOLDER, "Includes.xml")
TARGET = os.path.join(XMLFOLDER, "Includes.xml")
movefile()
SOURCE = os.path.join(WORKINGFOLDER, "IncludesBackgroundBuilding.xml")
TARGET = os.path.join(XMLFOLDER, "IncludesBackgroundBuilding.xml")
movefile()
SOURCE = os.path.join(WORKINGFOLDER, "MyVideoNav.xml")
TARGET = os.path.join(XMLFOLDER, "MyVideoNav.xml")
movefile()
# copy files from smashing
if os.path.exists(NEWFILES):
    contents = []
    contents = os.listdir(NEWFILES)
    size = len(contents)
    c = 0
    while c < size:
        item = contents[c]
        SOURCE = os.path.join(NEWFILES, item)
        TARGET = os.path.join(XMLFOLDER, item)
        if os.path.isfile(SOURCE):
            if os.path.isfile(TARGET):
                newname = 'a.default.' + item
                RENAMED = os.path.join(XMLFOLDER, newname)
                if os.path.exists(RENAMED):
                    try:
                        os.remove(RENAMED)
                        xbmc.sleep(300)
                    except:
                        printstar()
                        print 'Problem with xonfedit.py'
                        print 'Could not delete file'
                        print ('problem file = %s'% RENAMED)
                        print 'Make sure any incomplete skin edits are removed'
                        printstar()
                        xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
                        exit()            
                try:
                    os.rename(TARGET, RENAMED)
                except:
                    printstar()
                    print 'Problem with xonfedit.py'
                    print 'Could not move file'
                    print 'Make sure any incomplete skin edits are removed'
                    print ('sourcefile = %s'% TARGET)
                    print ('targetfile = %s'% RENAMED)
                    printstar()
                    xbmc.executebuiltin('Notification(Problem with xonfedit.py, Check log for details)')
                    exit()
                xbmc.sleep(300)
            copyfile()
            c = c + 1
#SOURCE = SETSVIEW
#TARGET = os.path.join(XMLFOLDER, "ViewMediaInfoSets.xml")
#copyfile()


xbmc.executebuiltin('ReloadSkin()')

xbmc.executebuiltin('Notification(All, done)')

# Drink beer



