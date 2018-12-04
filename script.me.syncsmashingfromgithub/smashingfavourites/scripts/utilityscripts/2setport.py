# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

ip = xbmc.getIPAddress()
printstar()
print "setport.py has just been started"
print ('IP is %s' % ip)
#xbmc.executebuiltin('Notification(IP address is, %s)'% ip)
#printstar()


#json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
#json_query = unicode(json_query, 'utf-8', errors='ignore')
## response is eg >> json_query is {"id":1,"jsonrpc":"2.0","result":{"name":"Kodi","version":{"major":17,"minor":4,"revision":"20170717-b22184d","tag":"releasecandidate","tagversion":"1"}}}
#start = 'major":'
#finish = ',"minor'
#version = (json_query.split(start))[1].split(finish)[0]
json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "services.webserverport"}, "id": 1 }')
print 'json_query is:'
print json_query
# response is eg >> {"id":1,"jsonrpc":"2.0","result":{"value":8080}}
start = '"value":'
finish = '}}'
currentport = (json_query.split(start))[1].split(finish)[0]
currentport = int(currentport)
print ('current port is %d'% currentport)
xbmc.executebuiltin('Notification(IP address is %s, webserver port is %d)'% (ip, currentport))
endip = ip[-2:]
if endip[:1] == '.':
    endip = endip[1:]
endip = int(endip)
print ('endip = %d'% endip)
wantedport = 10000 + endip
print ('wantedport = %d'% wantedport)
if not wantedport == currentport:
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"services.webserverport","value":%d},"id":1}'% wantedport)
    xbmc.executebuiltin('Notification(Webserver port changed to, %d)'% wantedport)
else:
    xbmc.executebuiltin('Notification(No action, required)')
printstar()
