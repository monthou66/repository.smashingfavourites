# -*- coding: utf-8 -*-
# get masterprofile
import xbmc
import os
import system

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGSPECIFICS = os.path.join(USERDATA, "smashing", "smashingspecifics")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "rsyncscripts")
# shellfile = os.path.join(folder, "rsyncstoragetousb.sh")

# get arguments
src = sys.argv[1]
# print ('src is %s'% src)
dest = sys.argv[2]
# print ('dest is %s'% dest)

# Get source and destination dirs.
if src = 'storage':
    source = '/storage'
elif src == '/storage':
    source = '/storage'
elif src == 'smashingfavourites':
    source = SMASHING
elif src == 'smashingspecifics':
    source = SMASHINGSPECIFICS
elif src == 'flash':
    if dest == 'storage':
        source = '/flash/stuff/backups/storage'
    elif dest == 'kodi':
        source = '/flash/stuff/backups/storage/.kodi'
    elif dest == 'smashingfavourites':
        source = '/flash/stuff/backups/storage/.kodi/userdata/smashing/smashingfavourites'
    elif dest == 'smashingspecifics':
        source = '/flash/stuff/backups/storage/.kodi/userdata/smashing/smashingspecifics'
    else:
        xbmcgui.Dialog().ok('     Source not recognised.', '     Action cancelled.')
        exit()
else:
    xbmcgui.Dialog().ok('     Source not recognised.', '     Action cancelled.')
    exit()

if dest == '

	
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
else:
    xbmc.executebuiltin('Notification(noway, jose)')

	
printstar()
print "startrsync.py has just been started"
print ('src is %s'% src)
print ('dest is %s'% dest)
printstar()