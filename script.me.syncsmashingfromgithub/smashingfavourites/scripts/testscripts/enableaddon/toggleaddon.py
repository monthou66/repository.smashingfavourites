#!/usr/bin/python
# -*- coding: utf-8 -*-
# startpvr.py

import xbmc
import json

# get arguments - to find which addon to toggle
markeraddon = sys.argv[1]

xbmc.executebuiltin( 'UpdateLocalAddons' )
if xbmc.getCondVisibility('System.HasAddon(%s)'% markeraddon):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":false}}'% markeraddon)
else:
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}'% markeraddon)
	