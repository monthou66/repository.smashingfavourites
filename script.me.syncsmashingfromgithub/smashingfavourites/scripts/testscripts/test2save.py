# -*- coding: utf-8 -*-
# move advancedsettings in/out - restart
import xbmc
import xbmcgui
import os
import sys
import shutil
import socket

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# Stop if problems with existing advancedsettings.xml
def checkxml():
    printstar()
    print 'There is a problem with the existing advancedsettings.xml'
    print 'It does not follow the needed format in the end lines.'
    print 'Sort it out and try again.'
    print ('The first problem found is with %s' % problem)
    printstar()
    exit()

# Get hostname
host = socket.gethostname()

# Get os
if xbmc.getCondVisibility('system.platform.android'):
    PLATFORM = 'android'
elif xbmc.getCondVisibility('system.platform.linux'):
    PLATFORM = 'linux'
elif xbmc.getCondVisibility('system.platform.windows'):
    PLATFORM = 'windows'
else:
    SYSPLAT = sys.platform
    printstar()
    print ('God only knows what platform this is!  sys.platform reurns %s' % SYSPLAT)
    printstar()
    exit()
# log
printstar()
print 'Starting advancedsettings.py'
print ('Hostname is %s' % host)
print ('You\'re using %s' % PLATFORM)
printstar()

# path to advancedsettings folders:	
# FOLDERSPATH = os.path.join(xbmc.translatePath('special://masterprofile'), "advancedsettings")
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
FOLDERSPATH = os.path.join(SMASHINGFAVOURITES, "advancedsettings")
# ADVANCEDSETTINGS = os.path.join(xbmc.translatePath('special://masterprofile'), "advancedsettings.xml")
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
DATABASE = os.path.join(USERDATA, "Database")
# Check what's running now
# Open file, read details
if os.path.isfile(ADVANCEDSETTINGS):
# count lines in file
    with open(ADVANCEDSETTINGS) as foo:
        length = len(foo.readlines())
    lines = file(ADVANCEDSETTINGS, 'r').readlines()
    print ('length= %s' % length)
    # 2 lines up
    length = length - 3
    print ('length= %s' % length)
    k = lines[length].rstrip()
    printstar()
    print ('k = %s' % k)
    if k == 'platform:':
        plat = lines[-1].rstrip()
    else:
        problem = 'platform'
        checkxml()
    # 4 lines up
    length = length - 2
    k = lines[length].rstrip()
    if k == 'drives:':
        pos = length + 1
        j = lines[pos]
        drives = j.rstrip()
    else:
        problem = 'drives'
        checkxml()
    # 6 lines up
    length = length - 2
    k = lines[length].rstrip()	
    if k == 'localormysql:':
        localormysqldatabase = lines[-6].rstrip()
    else:
        problem = 'localormysqldatabase'
        checkxml()
    # 8 lines up
    length = length - 2
    k = lines[length].rstrip()
    if k == 'source machine:':
        source = lines[-8].rstrip()
    else:
        problem = 'source'
        checkxml()
    # 10 lines up
    length = length - 2
    k = lines[length].rstrip()
    if k == '		<loglevel>1</loglevel>':			
        debug = 'enabled'
    elif k == '		<loglevel>0</loglevel>':
        debug == 'not enabled'
    else:
        problem = 'debug'
        checkxml()
    printstar()
    print ('Currently using %s' % drives)
    print ('Database is %s' % localormysqldatabase)
    print ('The drives are located on %s' % source)
    print ('Debug logging - %s' % debug)
    printstar()
else:
    printstar()
    print 'No advancedsettings.xml file is in place.'

# Label texturesxx.db and Thumbnails as local / mysql.server - to swap out via shell script if necessary
# Get database version (video / textures) - to check using right ones on swap


# Make a list of the available options:
ADVSETTS = []
test = []
for i in os.listdir(FOLDERSPATH):
    if os.path.isdir(os.path.join(FOLDERSPATH,i)):
# openadvsettings, read bottom lines to identify
        TARGETFILE = os.path.join(FOLDERSPATH,i,'advancedsettings.xml')
        if os.path.isfile(TARGETFILE):
#        if os.path.isfile(os.path.join(FOLDERSPATH,i,'advancedsettings.xml')):
            lines = file(TARGETFILE, 'r').readlines()
            tst = lines[-1].rstrip()
            test = tst.split('.')
            printstar()
            print ("tst returns as %s" % tst)
            print ("test returns as %s" % test)
            printstar()
            if len(test) == 5:
                box = test[0]
                location = test[1]
                db = test[2]
                drives = test[3]
                opera = test[4]
                if box == PLATFORM or box == host or box == 'All':
                    ADVSETTS.append(i)
            




n = len(ADVSETTS)
print ("There are %d available advancedsettings options." % n)
if n == 0:
    printstar()
    print "No advanced settings available"
    printstar()
    exit()

# Display list and get choice
CHOOSE = xbmcgui.Dialog().select("Options", ADVSETTS)
CHOICE = ADVSETTS[CHOOSE]
printstar()
print ("Choice = %s" % CHOICE)
printstar()
NEWADVSETTS = os.path.join(FOLDERSPATH, CHOICE, "advancedsettings.xml")
if os.path.isfile(NEWADVSETTS):
    os.remove(ADVANCEDSETTINGS)
    shutil.copy(NEWADVSETTS, USERDATA)
    printstar()
    print "New advanced settings loaded"
    printstar()
exit()


# Check each addon - if not enabled try enable, then check status again.  Report success or fail.
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
                SUCCESS.append(CHECK)
            else:
                e = e + 1
                FAIL.append(CHECK)				
        c = c + 1
# If any failures put a message on the screen.
ERROR = len(FAIL)
if ERROR > 0:
    xbmcgui.Dialog().ok('Some addons were not enabled.', 'Check your log for details.')

# print results to log
printstar()
print ("%s addons were checked" % n)
print ("%s addons were enabled" % d)
print ("There were %s failures" % e)
print ("Enabled addons: %s" % SUCCESS)
print ("Failures: %s" % FAIL)
printstar()
exit()

# Drink beer