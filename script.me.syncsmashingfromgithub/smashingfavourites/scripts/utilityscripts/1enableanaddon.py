# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# path to kodi addons folder:	
PATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
# Make some lists:
ADDONS = []
DISABLED = []
ENABLED = []
NOTFOUND = []

# Check current state:
xbmc.executebuiltin( 'UpdateLocalAddons' )

# Exclude addons I don't want to check - packages folder, temp folder obviously)
for i in os.listdir(PATH):
    if os.path.isdir(os.path.join(PATH,i)) and 'packages' not in i and 'temp' not in i:
        ADDONS.append(i)
printstar()
print ADDONS
n = len(ADDONS)
print ("There are %d addons in the kodi addons folder that will be checked." % n)
printstar()
# Check each addon - if not enabled add to DISABLED, if enabled add to ENABLED - otherwise add to NOTFOUND.
if n > 0:
    c = 0

    while c < n:
        CHECK = ADDONS[c]
        print ("Now checking %s ." % CHECK)
        if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
            ENABLED.append(CHECK)
        else:
            # is addonid same as foldername?  If not get id from addon.xml and try again!        
            ADDONXML = os.path.join(PATH, CHECK, "addon.xml")
            # get the addonid
            with open(ADDONXML) as f:
                for line in f:
                    if "<addon id=" in line:
                        start = "<addon id=\""
                        end = "\""
                        ADDONID = (line.split(start))[1].split(end)[0]
                        print ('Folder is %s' % CHECK)
                        print ('Addonid to check is %s' % ADDONID)
                        if not CHECK == ADDONID:
                            if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDONID):
                                ENABLED.append(ADDONID)
                            else:
                                DISABLED.append(ADDONID)
                        else:
                            DISABLED.append(CHECK)
        c = c + 1
    d = len(DISABLED)
    e = len(ENABLED)
    # check all addons are accounted for
    if not n == d + e:
        xbmc.executebuiltin('Notification(problem with enableanaddon.py, check log for details)')
        printstar()
        print 'Problem with enableanaddon.py.'
        print ('n = %d'% n)
        print ('d = %d'% d)
        print ('e = %d'% e)
        print 'So d + e != n'
        print ADDONS
        print ENABLED
        print DISABLED
       
        printstar()
        exit()
else:
    xbmc.executebuiltin('Notification(No addons, installed to check)')        
    printstar()
    print 'No addons installed to check.'
    printstar()
    exit()

if d == 0:
    xbmc.executebuiltin('Notification(No addons, are currently disabled)')
    printstar()
    print 'No disabled addons found'
    printstar()
    exit()

# testing
print ('Disabled addons are %s'% DISABLED)
g = 0
while g < d:
    thingy = DISABLED[g]
    print ('when g = %d:'% g)
    print ('addon is %s'% thingy)
    g = g + 1

    
# List disabled addons, so can choose one to enable
# Display list and get choice
CHOOSE = xbmcgui.Dialog().select("Choose an addon to enable", DISABLED)
# if don't select CHOOSE is -1, which selects last item.
if CHOOSE == -1:
    xbmc.executebuiltin('Notification(No addon, selected)')
    exit()
CHOICE = DISABLED[CHOOSE]
printstar()
print ('Choose is %d'% CHOOSE)
print ("Choice = %s" % CHOICE)
printstar()
if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHOICE)
    xbmc.sleep(200)
if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
    xbmc.executebuiltin('Notification(Oops, That did nuffin)')
else:
    xbmc.executebuiltin('Notification(Addon, has been enabled)')
exit()


# Drink beer