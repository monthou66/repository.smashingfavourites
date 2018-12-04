#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import json

def json_query(query):
    xbmc_request = json.dumps(query)
    result = xbmc.executeJSONRPC(xbmc_request)
    
#u'Fortuna Düsseldorf'.encode('utf8')    
#    result = result.encode('utf-8')
    
#    result = unicode(result, 'utf-8', errors='ignore')
    return json.loads(result)
    
def recordaudioposition():
  global playlist
  # get playlist
  get_music_playlist_contents = {"jsonrpc":"2.0", "id":1, "method":"Playlist.GetItems","params":{"playlistid":0,"properties":["file"]}}
  res = json_query(get_music_playlist_contents)
  if res.get('result',False):
    if res['result'].get('items',False):
      items = []
      for i in res['result']['items']:
#        items.append((i['id'],i['file']))
        items.append(i['file'])
      items.sort()
      lastitem = items[-1]
#      return 'music_-|-_' + '_-|-_'.join([x[1] for x in items])
      playlist = 'music_-|-_' + '_-|-_'.join([x for x in items]) 
      
    
recordaudioposition()
print 'playlist is:'
print playlist    
    
    
        
    
    
xbmc.executebuiltin('Notification(All, done)')



exit()