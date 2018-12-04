# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os

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
	
# Get running skin
SKIN = xbmc.getSkinDir()
skincomment = "You're using %s" %(skindir)
skinswitchplease = "Switch to Xonfluence and try again."
# Function = backup, newbackup, restore
FUNCTION = sys.argv(1)
XONFOPTION = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/xonfoption.txt")
SETTINGS = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/settings.xml")

# check xonfluence is running if backup or newbackup are selected.
def skincheck():
    if SKIN != "skin.xonfluence":
        xbmcgui.Dialog().ok(skincomment, skinswitchplease)
        exit()
	
def backupexistscheck():
    if os.path.exists(XONFOPTION):
        f = open(XONFOPTION)
        g = (f.read())		
        h = len(g)
        if h > 0:
            OPTION = h
			CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s .txt" % OPTION)
                if not os.path.exists(CHECK):
                    os.remove(XONFOPTION)
                    makeoptionstuff()
        else:
            os.remove(XONFOPTION)
            makeoptionstuff()
    else:
        makeoptionstuff()
            		
def makeoptionstuff():
    keyboard = xbmc.Keyboard("", "Enter backup name", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        OPTION = keyboard.getText()
        if xbmcgui.Dialog().yesno("Backup Xonfluence","to %s","Confirm?" % OPTION):
            make = open(XONFOPTION, 'w')
            make.write("%s" % OPTION)
            make.close()
            CHECK = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s .txt" % OPTION)
            produce = open(CHECK, 'w')
            produce.close()
            FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "addon_data/skin.xonfluence/ %s" % OPTION)
            if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
        else:
            forgetit()
    else:
        forgetit()
			
def forgetit():            
    printstar()
    printproblem()
    printabandon()	
    printnobackup()
    printstar()
    exit()
	
def cantfindfavourites():
    printstar()
    printproblem()
    printnobackup()
    print "Can't find xonfluence favourites file.  Backup cancelled."
    printstar()
    exit()

def backupxonf():
    shutil.copy(XONFOPTION, FOLDER)
    shutil.copy(CHECK, FOLDER)    
    shutil.copy(SETTINGS, FOLDER)
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
            cantfindfavourites()

			
			# make new line at the end of favourites file - restore OPTION
# taken from testfile4 on kryptonmess aspire - working

# OPTION = 'testytesty'
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
exit()

#ends

# xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite"
# eg <favourite name="Restore OPTION">RunScript(special://masterprofile/smashing/smashingfavourites/scripts/skinscripts/smashingxonfluence.py, restore, OPTION)</favourite>	
# xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title":"%s", "type":"media", "path":"%s", "thumbnail":"%s"}, "id": 1}' % (name, cmd, thumb)))
# xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title":"Restore %s", "type":"script", "path":"special://masterprofile/smashing/smashingfavourites/scripts/skinscripts/smashingxonfluence.py, restore, OPTION", "thumbnail":""}, "id": 1}' % (OPTION))	
def stopxonf():






def restorexonf():



def removebackup():


if skindir == "skin.xonfluence":
    skinchoice = "Good choice"
else:
    skinchoice = "Stoopid arse"
	
skincomment = "You're using %s" %(skindir)	
xbmcgui.Dialog().ok(skinchoice, skincomment)
xbmc.sleep(5000)

# end my bit

keyboard = xbmc.Keyboard("", "Type your name", False)
keyboard.doModal()
if keyboard.isConfirmed() and keyboard.getText() != "":
    line1 = "Hello World!"
    line2 = "Nice to meet you %s" %(keyboard.getText())
    line3 = "Welcome to Kodi!"
    xbmcgui.Dialog().ok("bozo", line1, line2, line3)
#    xbmcgui.Dialog().ok(addonname, line1, line2, line3)





import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
PATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
ADDONS = []
for i in os.listdir(PATH):
    if os.path.isdir(os.path.join(PATH,i)) and 'packages' not in i and 'pvr' not in i and 'metadata' not in i:
        ADDONS.append(i)
printstar()
print ADDONS
n = len(ADDONS)
print ("There are %d addons in the folder" % n)
if n > 0:
    c = 0
    d = 0
    e = 0
    while c < n:
        CHECK = ADDONS[c]
        print ("Now checking %s ." % CHECK)
        if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHECK)
            xbmc.sleep(200)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
                d = d + 1
            else:
                e = e + 1			
        c = c + 1
print ("%s addons were checked" % n)
print ("%s addons were enabled" % d)
print ("There were %s failures" % e)
exit()

# xbmc.executebuiltin( 'UpdateLocalAddons' )

import xbmc
import xbmcaddon
import xbmcgui
 
#addon       = xbmcaddon.Addon()
#addonname   = addon.getAddonInfo('name')

#my bit
skindir = xbmc.getSkinDir()
if skindir == "skin.xonfluence":
    skinchoice = "Good choice"
else:
    skinchoice = "Stoopid arse"
	
skincomment = "You're using %s" %(skindir)	
xbmcgui.Dialog().ok(skinchoice, skincomment)
xbmc.sleep(5000)

# end my bit

keyboard = xbmc.Keyboard("", "Type your name", False)
keyboard.doModal()
if keyboard.isConfirmed() and keyboard.getText() != "":
    line1 = "Hello World!"
    line2 = "Nice to meet you %s" %(keyboard.getText())
    line3 = "Welcome to Kodi!"
    xbmcgui.Dialog().ok("bozo", line1, line2, line3)
#    xbmcgui.Dialog().ok(addonname, line1, line2, line3)

# http://mirrors.xbmc.org/docs/python-docs/stable/xbmc.html