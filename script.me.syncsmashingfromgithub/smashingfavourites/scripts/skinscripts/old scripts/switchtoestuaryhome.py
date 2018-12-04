#!/usr/bin/python
# -*- coding: utf-8 -*-
#import xbmc,xbmcgui,xbmcplugin
import xbmc

xbmc.executebuiltin("ActivateWindow(Home)")
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.estuary"}}')
xbmc.executebuiltin('SendClick(11)')