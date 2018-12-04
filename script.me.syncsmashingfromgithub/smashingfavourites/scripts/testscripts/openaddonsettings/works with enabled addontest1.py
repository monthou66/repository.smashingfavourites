#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

print 'running test1.py'

# xbmcaddon.Addon('pvr.dvbviewer').openSettings()

#thingy = 'pvr.iptvsimple'
thingy = 'pvr.dvbviewer'

#xbmc.executebuiltin('Addon.OpenSettings(%s)'% thingy)
# Addon.OpenSettings('pvr.dvbviewer')

# xbmcaddon.Addon().openSettings() 

xbmcaddon.Addon('%s'% thingy).openSettings() 




message = ('All, done')
xbmc.executebuiltin('Notification(%s)'% message)
exit()
# responses
# group = Group: All channels
# group =