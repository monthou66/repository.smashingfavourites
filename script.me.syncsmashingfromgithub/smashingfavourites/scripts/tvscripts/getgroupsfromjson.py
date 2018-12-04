# -*- coding: utf-8 -*-

import xbmc
import json
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test2.py has just been started"
printstar()
#xbmc.executebuiltin('Notification(test2.py, started)')
CHANNELGROUPS = []

ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
channelgroups = ret['result']['channelgroups']
for channelgroup in channelgroups:
    printstar()
    print channelgroup
    chanstring = str(channelgroup)
    start = "u'label': u'"
    end = "'}"		
    group = (chanstring.split(start))[1].split(end)[0]
    CHANNELGROUPS.append(group)
print CHANNELGROUPS
numb = len(CHANNELGROUPS)
print ('There are %d channel groups' % numb)
c = 0
while c < numb:
    print CHANNELGROUPS[c]
    c = c + 1
printstar()