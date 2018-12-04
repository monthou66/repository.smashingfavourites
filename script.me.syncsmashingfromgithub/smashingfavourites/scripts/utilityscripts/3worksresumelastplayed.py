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
    global next, type, top, btm
    print 'running resume()'
    # defaults
    top = 'not set'
    btm = 'not set'
    # clear current playlist                #### or it grows exponentially!!!
    xbmc.executebuiltin('Playlist.Clear')
    if os.path.isfile(PATH):
        f = open(PATH,"r")
        lines = f.readlines()
        try:
            mediaFile = lines[0].strip()
        except:
            mediaFile = 'not set'
        try:
            title = lines[1].strip()
        except:
            title = 'not set'
        try:
#            position = float(lines[2]).strip()
            position = lines[2].strip()
        except:
            position = 'not set'
#        itemduration = float(lines[3]).strip()
        try:
            itemduration = lines[3].strip()
        except:
            itemduration = 'not set'
        if position == 'not set':
            position = 0
        elif itemduration == 'not set':
            position = 0
        else:
            position = float(position)
#            top = int(position)
            top = round(position)
            btm = int(itemduration)
            percentageplayed = 100 * top / btm
        # get playlist
        try:
            playlist = lines[4].split('_-|-_')
        except:
            playlist = []
        if not len(playlist) > 1:
            try:
                # Play file.
                xbmc.Player().play(mediaFile)
            except:
                xbmc.executebuiltin('Notification(Problem playing file, check log for details)')
                print ('Problem playing mediaFile: %s'% mediaFile)
        else:
            # load playlist
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
            # play file
            try:
                xbmc.Player().play(xbmc.PlayList(add_this['params']['playlistid']), startpos=playlist_position)
            except:
                xbmc.executebuiltin('Notification(Problem starting playlist, check log for details)')
                print ('Problem in resume(): starting playlist')
        # wait 10 seconds for playback to start
        c = 0
        while c < 50:
            if (not xbmc.Player().isPlaying()):
                xbmc.sleep(200)
                if c == 5:
                    xbmc.executebuiltin('Notification(Starting, playback)')
                c = c + 1
            else:
                c = 500
        if c < 500:
            xbmc.executebuiltin('Notification(Playback, cancelled)')
        else:
            # Seek to last recorded position.
            xbmc.Player().seekTime(position)
            xbmc.sleep(1000)
            # Make sure it actually got there.
            if abs(position - xbmc.Player().getTime()) > 30:
                xbmc.Player().seekTime(position)
            # show info at start of playback (video only)
            if xbmc.getCondVisibility('Player.HasVideo'):
                xbmc.executebuiltin( "XBMC.Action(Info)" )
                xbmc.sleep(5000)
                xbmc.executebuiltin( "XBMC.Action(Info)" )
            elif xbmc.getCondVisibility('Player.HasAudio'):
                xbmc.executebuiltin('Notification(Resuming, playlist)')
      
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