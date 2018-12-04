#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc

if not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
    if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):	
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":false}}')
        xbmc.sleep(1000)
    if xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):		
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')	
        xbmc.sleep(10000)
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":true}}')
    xbmc.sleep(10000)
xbmc.executebuiltin('ActivateWindow(TVChannels)')	
