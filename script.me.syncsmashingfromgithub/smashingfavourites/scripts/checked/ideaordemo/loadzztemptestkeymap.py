# -*- coding: utf-8 -*-
import os
import os.path
import xbmc
import xbmcaddon
import xbmcvfs

# copy keymap to keymaps folder
# reload keymaps
# Start with argument (keymap name) from remote or shortcut
FILE = sys.argv[1]

#define source / destination
KEYMAPSOURCEFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/scripts/smashingkeymaps/ %s .xml" % FILE)
KEYMAPDESTFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "keymaps/ %s .xml" % FILE)

#  Check if FILE is a valid keymap, copy it to keymaps folder and reload keymaps

if os.path.isfile(KEYMAPSOURCEFILE):
    xbmcvfs.copy(KEYMAPSOURCEFILE, KEYMAPDESTFILE)
    xbmc.executebuiltin('Action(reloadkeymaps)')
    xbmc.sleep(300)
    xbmc.executebuiltin('Notification(keymap, loaded)')
    exit()
else:
    xbmc.executebuiltin('Notification(Problem, keymap not loaded)')
    exit()