#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc

if xbmc.getCondVisibility('System.HasPVRAddon'):
    if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')
        xbmc.sleep(10000)
        if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):	
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":false}}')
            xbmc.sleep(10000)
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":true}}')
            xbmc.sleep(10000)
#            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":false}}')			












