def get_installedversion():
    global json_query, version
    # retrieve current installed version
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    # response is eg >> json_query is {"id":1,"jsonrpc":"2.0","result":{"name":"Kodi","version":{"major":17,"minor":4,"revision":"20170717-b22184d","tag":"releasecandidate","tagversion":"1"}}}
    start = 'major":'
    finish = ',"minor'
    version = (json_query.split(start))[1].split(finish)[0]
    
# get settings    
json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "services.webserverport"}, "id": 1 }')
print 'json_query is:'
print json_query
# response is eg >> {"id":1,"jsonrpc":"2.0","result":{"value":8080}}
start = '"value":'
finish = '}}'
currentport = (json_query.split(start))[1].split(finish)[0]
currentport = int(currentport)
print ('current port is %d'% currentport)


# set settings
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"services.webserverport","value":%d},"id":1}'% wantedport)


autoplay = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "musicplayer.autoplaynextitem"}, "id": 1 }')
print 'autoplay is:'
print autoplay              # returns:  {"id":1,"jsonrpc":"2.0","result":{"value":true}}
xbmc.sleep(300)
autoplaystatus = "false"
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"musicplayer.autoplaynextitem","value":%s},"id":1}'% autoplaystatus)

