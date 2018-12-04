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
CHANNELSLIST = []

ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
channelgroups = ret['result']['channelgroups']
for channelgroup in channelgroups:
#Get Channels
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannels", "params":{"channelgroupid" : ' + str(channelgroup['channelgroupid']) + '} }'))
    channels = ret['result']['channels']
    for channel in channels:
#Get Channel Details
        ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelDetails", "params":{"channelid" : ' + str(channel['channelid']) + '} }'))
#        utils.write_log('service', str(ret)) 
#        printstar()
#        print('service', str(ret))
# try	get channel name from string	
        retstring = str(ret)
        start = "u'label': u'"		
        end = "'}}}"		
        CHANNEL = (retstring.split(start))[1].split(end)[0]		
        print ('Channel is %s' % CHANNEL)		
#        printstar()
# add channel name to list
        CHANNELSLIST.append(CHANNEL)
printstar()
print CHANNELSLIST
printstar()
print 'Channel groups:'
print channelgroups
printstar()		