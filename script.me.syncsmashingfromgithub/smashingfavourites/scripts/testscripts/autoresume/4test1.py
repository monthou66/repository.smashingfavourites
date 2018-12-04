#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import os
import json

ADDON = xbmcaddon.Addon('service.autoresume')
FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
PATH = os.path.join(FOLDER, 'testautoresume.txt')

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def stopped():
    print 'Not saving playlist details'
    xbmc.executebuiltin('Notification(Not, on your nelly)')
    exit()

def getinfo():
    global playlist, lastitem, mediaFile, title, position, itemduration, items
    mediaFile = 'not set'
    title = 'title not known'
    position = 'position not known'
    itemduration = 'duration not known'
    mediaFile = xbmc.Player().getPlayingFile()
    if mediaFile[:3] == 'pvr':
        stopped()
    elif mediaFile[:4] == 'http':
        stopped()
    try:
        title = xbmc.getInfoLabel('Player.Title')
    except:
        pass
    position = xbmc.Player().getTime()
    # get itemduration
    hours = xbmc.getInfoLabel('Player.Duration(hh)')
    hours = int(hours) * 3600
    minutes = xbmc.getInfoLabel('Player.Duration(mm)')
    minutes = int(minutes) * 60
    seconds = xbmc.getInfoLabel('Player.Duration(ss)')
    seconds = int(seconds)
    itemduration = hours + minutes + seconds
    items = []
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Playlist.GetItems", "params":{"playlistid":%s,"properties":["file"]} }'% type))
    files = ret['result']['items']   
    num = len(files)
    c = 0
    while c < num:
        f = files[c]
        fstring = str(f)
        start = "file': u'"
        end = "', u'label':"
        try:    
            next = (fstring.split(start))[1].split(end)[0]
        except:
            try:
                start = "file': u\""
                end = "\", u'label':"
                next = (fstring.split(start))[1].split(end)[0]
            except:        
                next = 'errored out'            # will still add to playlist but not play
        items.append(next)
        c = c + 1
    lastitem = items[-1]
    if type == '1':
        playlist = 'video_-|-_' + '_-|-_'.join([x for x in items])
    elif type == '0':
        playlist = 'music_-|-_' + '_-|-_'.join([x for x in items])
        
def writefile():
    with open(PATH, 'w') as f:
        f.write(mediaFile)
        f.write('\n')
        f.write(title)                          # gives: title not known
        f.write('\n')
        f.write(repr(position))                 # gives: 'position not known'
        f.write('\n')
        f.write(repr(itemduration))             # gives: 'duration not known'
        f.write('\n')
        f.write(playlist)

def json_query(query):
    xbmc_request = json.dumps(query)
    result = xbmc.executeJSONRPC(xbmc_request)
    result = unicode(result, 'utf-8', errors='ignore')
    return json.loads(result)
    
def resume():
    global next, type
    print 'running resume()'
    # clear current playlist                #### or it grows exponentially!!!
    xbmc.executebuiltin('Playlist.Clear')
    if os.path.isfile(PATH):
        f = open(PATH,"r")
        lines = f.readlines()
        mediaFile = lines[0].strip()
        title = lines[1].strip()
#        position = float(lines[2]).strip()
        position = lines[2].strip()
#        itemduration = float(lines[3]).strip()
        itemduration = lines[3].strip()
        position = float(position)
#        top = int(position)
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

        printstar()
        print ('mediaFile is %s'% mediaFile)
        print ('title is %s'% title)
        print ('position is %s'% position)
        print ('duration is %s'% itemduration)
        print ('top = %s'% top)
        print ('btm = %s'% btm)
        print ('percentage played = %d'% percentageplayed)
        print ('playlist is: %s'% playlist)
        if len(playlist) > 1:
            for x in playlist:
                print x
        printstar()
        
if xbmc.Player().isPlaying():
    if xbmc.getCondVisibility('Player.HasVideo'):
        type = '1'
#        start = 'video_-|-_'
    elif xbmc.getCondVisibility('Player.HasAudio'):
        type = '0'
#        start = 'music_-|-_' 
    print ('type is %s'% type)
    getinfo() 
    print ('type = %s'% type)
    print ('mediaFile is %s'% mediaFile)
    print ('Title is %s'% title)
    print ('position is %s'% position)
    print ('duration is %s seconds'% itemduration)
    print 'playlist is:'
    print playlist
    printstar()
    for x in items:
        print x
    printstar()
    writefile()
    xbmc.executebuiltin('Notification(All, done)')
else:

    autoplay = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "musicplayer.autoplaynextitem"}, "id": 1 }')
    print 'autoplay is:'
    print autoplay              # returns:  {"id":1,"jsonrpc":"2.0","result":{"value":true}}
    xbmc.sleep(300)
    autoplaystatus = "false"
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"musicplayer.autoplaynextitem","value":%s},"id":1}'% autoplaystatus)
    xbmc.sleep(300)
    autoplay = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "musicplayer.autoplaynextitem"}, "id": 1 }')
    print 'autoplay is now:'
    print autoplay              # returns:  


    
    
    # resume
    resume()

    exit()
    
    xbmc.sleep(300)
    autoplaystatus = "true"
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"musicplayer.autoplaynextitem","value":%s},"id":1}'% autoplaystatus)
    xbmc.sleep(300)
    autoplay = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "musicplayer.autoplaynextitem"}, "id": 1 }')
    print 'And now:'
    print autoplay              # returns:  

