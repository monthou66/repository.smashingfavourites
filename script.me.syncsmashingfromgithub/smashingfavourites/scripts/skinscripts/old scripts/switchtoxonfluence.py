#!/usr/bin/python
# -*- coding: utf-8 -*-
#import xbmc,xbmcgui,xbmcplugin
import xbmc

xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.xonfluence"}}')
xbmc.executebuiltin('SendClick(11)')
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skintheme","value":"gray"}}')
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skincolors","value":"gray"}}')