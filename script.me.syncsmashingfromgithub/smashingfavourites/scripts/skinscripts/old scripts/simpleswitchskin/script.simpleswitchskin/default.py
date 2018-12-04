#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
newskin = 'none'

if len(sys.argv) > 1:
    newskin = sys.argv[1]
if newskin == "none":
    xbmc.executebuiltin('Notification(Switch skin from a shortcut, Start script with new skinid or \'choose\' as the argument)')
elif newskin == 'choose':
    xbmc.executebuiltin('Addon.Default.Set(xbmc.gui.skin)')
elif xbmc.getCondVisibility('System.HasAddon(%s)'% newskin):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% newskin)
    xbmc.executebuiltin('SendClick(11)')
else:
    xbmc.executebuiltin('Notification(%s, is not enabled)'% newskin)
exit()