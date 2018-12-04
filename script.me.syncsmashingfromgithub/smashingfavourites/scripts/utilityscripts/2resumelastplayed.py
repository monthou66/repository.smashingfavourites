#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcvfs
import os
import json

# defaults
central = 'false'
centralpath = 'smb://192.168.1.1/smashing/smashingcentraltemp/'
filelocation = 'local'
ADDON = xbmcaddon.Addon('service.autoresume')
# FOLDER = ADDON.getSetting('autoresume.save.folder').encode('utf-8', 'ignore')
FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode("utf-8")
PATH = os.path.join(FOLDER, 'autoresume.txt')
if ADDON.getSetting('central.path.enable') == "true":
  central = 'true'
  if ADDON.getSetting('central.path') != "":
	centralpath = ADDON.getSetting('central.path').decode("utf-8")
centralfile = os.path.join(centralpath, 'autoresume.txt')

def startscript():
    global file, filelocation
    thisaddon = sys.argv[0]
    if len(sys.argv) > 1:
        filelocation = sys.argv[1]
    if filelocation == 'central':
        file = centralfile
    else:
        file = PATH
    print ('starting %s'% thisaddon)
#    print ('using %s file'% filelocation)
#    print ('file is %s'% file)

def json_query(query):
    xbmc_request = json.dumps(query)
    result = xbmc.executeJSONRPC(xbmc_request)
    result = unicode(result, 'utf-8', errors='ignore')
    return json.loads(result)

def centraltolocal():
  global PATH
  print 'running centraltolocal()'
  # copy the central file to the addon_data folder
  source = centralfile
  target = os.path.join(FOLDER, 'centralautoresume.txt')
  if os.path.exists(target):
    os.remove(target)
    xbmc.sleep(300)
  if xbmcvfs.exists(source):
    xbmcvfs.copy(source, target)
    PATH = target
    xbmc.executebuiltin('Notification(Starting autoresume, from central source)')
  else:
    xbmc.executebuiltin('Notification(Starting autoresume, from local source)')
    
def resume():
  for x in range(0,120):
    if os.path.exists(FOLDER):
      if os.path.exists(PATH):
        # Read from autoresume.txt.
        with open(PATH, 'r') as f:
          mediaFile = f.readline().rstrip('\n')
          position = float(f.readline())
          try:
            playlist = f.readline().split('_-|-_')
          except:
            playlist = []

        # load playlist contents
        if len(playlist) > 1:
          add_this = {'jsonrpc': '2.0','id': 1, "method": 'Playlist.Add', "params": {'item' : {'file' : 'placeholder' }, 'playlistid' : 'placeholder'}}

          if playlist[0] == 'music':
            add_this['params']['playlistid'] = 0
          else:
            add_this['params']['playlistid'] = 1

          for x in playlist[1:]:
            add_this['params']['item']['file'] = x
            json_query(add_this)

          try:
            playlist_position = playlist.index(mediaFile) - 1
          except:
            playlist_position = 0

          xbmc.Player().play(xbmc.PlayList(add_this['params']['playlistid']), startpos=playlist_position)

        else:
          # Play file.
          xbmc.Player().play(mediaFile)

        while (not xbmc.Player().isPlaying()):
          xbmc.sleep(500)
        xbmc.sleep(1000)
        # Seek to last recorded position.
        xbmc.Player().seekTime(position)
        xbmc.sleep(1000)
        # Make sure it actually got there.
        try:
            if abs(position - xbmc.Player().getTime()) > 30:
              xbmc.Player().seekTime(position)
        except:                                     # seek fails if file already stopped
            exit()
      break
    else:
      # If the folder didn't exist maybe we need to wait longer for the drive to be mounted.
      xbmc.sleep(5000)
      
startscript()
if not xbmc.Player().isPlaying():
  if filelocation == 'central':
    centraltolocal()
  else:
    xbmc.executebuiltin('Notification(Starting autoresume, from local source)')
  resume()
else:
  xbmc.executebuiltin('Notification(Stop playback, and try again)')
exit()