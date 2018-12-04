# -*- coding: utf-8 -*-

import xbmc
import json

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')

# json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.getSettings", "params": { "filter":{"section":"system", "category":"debug"} } }')

# json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.getSettings", "params": { "filter":{"section":"system"} } }')

# works for all settings
# json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.getSettings"} }')

# from audioprofiles
            # get all settings from System / Audio section
json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettings", "params":{"level": "expert", "filter":{"section":"system","category":"audio"}},"id":1}')

printstar()
print 'json_query is:'
print json_query
printstar()