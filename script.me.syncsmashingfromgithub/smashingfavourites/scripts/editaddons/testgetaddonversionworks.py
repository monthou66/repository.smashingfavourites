# -*- coding: utf-8 -*-
# testgetaddonversion.py


import xbmc
import xbmcaddon
import os

error = 'non-specific'
addon_path = 'not found yet'
addon_version = 'not found yet'
xml = 'not found yet'
error = 'non-specific'

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def errormessage():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    if not error == 'non-specific':
        print error
    printstar()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    exit()

def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

#def getarguments():
#    global

def getaddonid():
    global source, addon_path, addon_version
    source = 'Results from xbmcaddon.getAddonInfo:'
#    json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"level": "expert", "filter":{"section":"system","category":"audio"}},"id":1}')
#    json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails", "params":{'addonid': 'pvr.iptvsimple', 'properties': ['version']}},"id":0}')

#    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
#    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Addons.GetAddonDetails", "params":{"addonid":"pvr.iptvsimple"} }'))

#    channelgroups = ret['result']['channelgroups']    
#    ver = ret['result']['version']   


# only works if addon is enabled
    addon         = xbmcaddon.Addon(id='pvr.iptvsimple')
    addon_path    = addon.getAddonInfo('path')
    addon_version = addon.getAddonInfo('version')

def getaddonpath():
    global source, addon_path, addon_version
    source = 'Results from looking for folders:'
    addon = 'pvr.iptvsimple'
    addon_path = 'not found yet'
    addon_version = 'not found yet'    
    checkpath = os.path.join(xbmc.translatePath('special://home/addons/%s'% addon))
    alternatepath = os.path.join(xbmc.translatePath('special://xbmc/addons/%s'% addon))
    if os.path.exists(alternatepath):
        addon_path = alternatepath
    elif os.path.exists(checkpath):
        addon_path = checkpath
        
def getaddonversionfromxml():     
    global source, addon_path, addon_version, xml
    source = 'Results from reading addon.xml:'  
    
    # check 1
#    print ('check 1: addon_path is %s'% addon_path)

    if not addon_path == 'not found yet':
        xml = os.path.join(addon_path, 'addon.xml')

        with open(xml, 'r') as myfile:
            lines = myfile.readlines()
            checkline = lines[2]
#            print ('checkline is %s'% checkline)
            if 'version' in checkline:
                start = 'version="'
                end = '"'           
                addon_version = (checkline.split(start))[1].split(end)[0]
            else:
                error = ('Could not get addon version')
                errormessage()

def output():    
    printstar()
    print source
    print ('path is %s'% addon_path)
    print ('version is %s'% addon_version)
    if not xml  == 'not found yet':
        print ('addon.xml is located at %s'% xml)
#    print 'json_query is:'
#    print json_query
    printstar()    
    
    
    
startaddon()
getaddonid()
output()
getaddonpath()
output()
getaddonversionfromxml()
output()
exit()

# Drink beer



