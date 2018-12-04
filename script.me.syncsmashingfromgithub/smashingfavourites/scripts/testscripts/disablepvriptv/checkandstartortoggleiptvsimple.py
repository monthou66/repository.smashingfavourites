#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"

if xbmc.getCondVisibility('System.HasPVRAddon'):
    printstar()
    print 'check 1'
    if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')
        xbmc.sleep(1000)
        printstar()
        print 'check 2'
if not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
    printstar()
    print 'check 3'
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":true}}')	
#    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":true}}')
    printstar()
    print 'check 4'
printstar()
print 'check 5'












