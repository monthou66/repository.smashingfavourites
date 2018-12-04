# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os

# path to kodi addons folder:	
ADDONSPATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
DEFAULTADDONSPATH = os.path.join(xbmc.translatePath('special://xbmc/'), "addons")
# marker = os.path.join(xbmc.translatePath('special://masterprofile'), 'smashingtemp', 'markers', 'enableanaddonrunning.txt')
# Make some lists:
ADDONS = []
DISABLED = []
ENABLED = []
NOTFOUND = []

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
#    a = sys.argv[1]
    printstar()
    print ('%s has started'% thisaddon)
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

def getarguments():	
    global job, include, type, force
    job = 'enable'
    include = 'true'
    type = 'wibble'
    force = 'false'
    num = len(sys.argv)
    if num > 4:
        printstar()
        print ('Too many arguments when starting %s'% thisaddon)
        printstar()
        xbmc.executebuiltin('Notification(%s, stopped - check log)'% thisaddon)
    if num > 1:
        c = 0
        while c < num:
            arg = sys.argv[c]
            if arg == 'enable':
                job = 'enable'
            elif arg == 'disable':
                job = 'disable'
            elif arg == 'include':
                include = 'true'
            elif arg == 'exclude':
                include = 'false'
            elif arg == 'force':
                force = 'true'
            else:
                type = arg
            c = c + 1
    # check
    print 'check 55'
    print ('job is %s'% job)
    print ('include is %s'% include)
    print ('type is %s'% type)

def oldgetarguments():	
    global job, include, type
    job = 'enable'
    include = 'wibble'
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
    if arg1 == 'enable':
        job = 'enable'
    elif arg1 == 'disable':
        job = 'disable'
    else:
        if arg1 == 'include':
            include = 'true'
            if len(sys.argv) > 2:
                type = sys.argv[2]
            else:
                include = 'wibble'
        elif arg1 == 'exclude':
            include = 'false'
            if len(sys.argv) > 2:
                type = sys.argv[2]
            else:
                include = 'true'
                type = sys.argv[1]
                

def listaddons():
    global ADDONS
    # Exclude addons I don't want to check - packages folder, temp folder obviously)
    for i in os.listdir(PATH):
        if not i[0:5] == 'xbmc.':
            if type == 'wibble':
                if os.path.isdir(os.path.join(PATH,i)) and 'packages' not in i and 'temp' not in i:
                    ADDONXML = os.path.join(PATH, i, "addon.xml")
                    if os.path.exists(ADDONXML):
                        if i not in ADDONS:
                            ADDONS.append(i)
            elif include == 'true':
                if os.path.isdir(os.path.join(PATH,i)) and type in i and 'packages' not in i and 'temp' not in i:
                    ADDONXML = os.path.join(PATH, i, "addon.xml")
                    if os.path.exists(ADDONXML):
                        if i not in ADDONS:
                            ADDONS.append(i)
            elif include == 'false':
                if os.path.isdir(os.path.join(PATH,i)) and type not in i and 'packages' not in i and 'temp' not in i:
                    ADDONXML = os.path.join(PATH, i, "addon.xml")
                    if os.path.exists(ADDONXML):
                        if i not in ADDONS:
                            ADDONS.append(i)

def checkaddons(): 
    global ENABLED, DISABLED               
    printstar()
    print ADDONS
    n = len(ADDONS)
    print ("There are %d addons in the kodi addons folders that will be checked." % n)
    printstar()
    # Check each addon - if not enabled add to DISABLED, if enabled add to ENABLED - otherwise add to NOTFOUND.
    if n > 0:
        c = 0
        while c < n:
            CHECK = ADDONS[c]
            print ("Now checking %s ." % CHECK)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
                if CHECK not in ENABLED:
                    ENABLED.append(CHECK)
            else:
                # is addonid same as foldername?  If not get id from addon.xml and try again!        
                ADDONXML = os.path.join(ADDONSPATH, CHECK, "addon.xml")
                if not os.path.exists(ADDONXML):
                    ADDONXML = os.path.join(DEFAULTADDONSPATH, CHECK, "addon.xml")
                # get the addonid
                with open(ADDONXML) as f:
                    for line in f:
                        if 'id="' in line:
#                        if "<addon id=" in line:
                            start = "id=\""
                            end = "\""
                            ADDONID = (line.split(start))[1].split(end)[0]
                            print ('Folder is %s' % CHECK)
                            print ('Addonid to check is %s' % ADDONID)
                            if not CHECK == ADDONID:
                                if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDONID):
                                    if ADDONID not in ENABLED:
                                        if ADDONID not in DISABLED:
                                            ENABLED.append(ADDONID)
                                else:
                                    if ADDONID not in DISABLED:
                                        if ADDONID not in ENABLED:
                                            DISABLED.append(ADDONID)
                            else:
                                if CHECK not in DISABLED:
                                    if CHECK not in ENABLED:
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
        if job == 'enable':
            xbmc.executebuiltin('Notification(No relevant addons, are currently disabled)')
            printstar()
            print 'No relevant disabled addons found'
            printstar()
            exit()
            
    if e == 0:
        if job == 'disable':
            xbmc.executebuiltin('Notification(No relevant addons, are currently enabled)')
            printstar()
            print 'No relevant enabled addons found'
            printstar()
            exit()

def test():
    # testing
    print ('Disabled addons are %s'% DISABLED)
    g = 0
    while g < d:
        thingy = DISABLED[g]
        print ('when g = %d:'% g)
        print ('addon is %s'% thingy)
        g = g + 1
        
    print ('Enabled addons are %s'% ENABLED)
    g = 0
    while g < d:
        thingy = ENABLED[g]
        print ('when g = %d:'% g)
        print ('addon is %s'% thingy)
        g = g + 1        

def chooseaddontoenable():
    if force == 'true' and len(DISABLED) == 1:
        CHOOSE = 0
        CHOICE = DISABLED[0]
    else:
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
        
def chooseaddontodisable():
    if force == 'true' and len(ENABLED) == 1:
        CHOOSE = 0
        CHOICE = ENABLED[0]
    else:
        # List enabled addons, so can choose one to disable
        # Display list and get choice
        CHOOSE = xbmcgui.Dialog().select("Choose an addon to disable", ENABLED)
        # if don't select CHOOSE is -1, which selects last item.
        if CHOOSE == -1:
            xbmc.executebuiltin('Notification(No addon, selected)')
            exit()
        CHOICE = ENABLED[CHOOSE]
    printstar()
    print ('Choose is %d'% CHOOSE)
    print ("Choice = %s" % CHOICE)
    printstar()
    if xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":false}}' % CHOICE)
        xbmc.sleep(200)
    if xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
        xbmc.executebuiltin('Notification(Oops, That did nuffin)')
    else:
        xbmc.executebuiltin('Notification(Addon, has been disabled)')
    
startaddon()
getarguments()
# Check current state:
xbmc.executebuiltin( 'UpdateLocalAddons' )
PATH = ADDONSPATH
listaddons()
PATH = DEFAULTADDONSPATH
listaddons()
checkaddons()
if job == 'enable':
    if len(DISABLED) > 0:
        chooseaddontoenable()
    else:
        print 'No addon to enable'
        xbmc.executebuiltin('Notification(No installed Addon, needs to be enabled)')
elif job == 'disable':
    if len(ENABLED) > 0:
        chooseaddontodisable()
    else:
        print 'No addon to disable'
        xbmc.executebuiltin('Notification(No Addon, needs to be disabled)')
exit()


# Drink beer