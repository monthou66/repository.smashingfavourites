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

def errornot():
    global fstring, z
    xbmc.executebuiltin('Notification(Oh, bugger)')
    print ('fstring is %s'% fstring)
    if '\\xf1' in fstring:
        fstring.replace('\\xf1', 'ñ')  
        print 'replaced'
        print ('fstring is now %s'% fstring)
        z = fstring.decode('Latin-1')
        print ('z is %s'% z)
        
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
    
    print 'files:'
    for z in files:
        y = str(z)
        x = y.encode('latin-1', 'ignore')
        print z
        print y
        print x
    
    
    num = len(files)
    c = 0
    while c < num:
        f = files[c]
        fstring = str(f)
        start = "file': u'"
        end = "', u'label':"
        try:    
            next = (fstring.split(start))[1].split(end)[0]
            next = unicode(next, 'utf-8', errors='ignore')
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
        
def loadplaylist():
#    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Playlist.Add", "params":{"item" : {"file" : '%s' }, "playlistid" : '%s'}},"id":1}'% (next, type))
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Playlist.Add", "params":{"item" : "file" : "%s", "playlistid" : "%s"},"id":1}'% (next, type))

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
        print 'check116'
        
        f = open(PATH,"r")
#        f = open(the_list[0][u'file'])


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
            # check for dodgy filenames
            length = len(playlist)
            v = 1
            print 'check146'
            while v < length:
                testfile = playlist[v]
                if not xbmcvfs.exists(testfile):
                    print ('Can\'t find file: %s'% testfile)
                    xbmc.executebuiltin('Notification(Problem, check log)')
                    if "/" in testfile:
                        end = "/"
#                        testfolder = testfile.split(end)[0]                 # gives       smb:
#                        testfolder = testfile.rsplit(end, 1)[0]             # gives       smb://Source Music/OSTs/Guardians of the Galaxy - Awesome Mix Vol. 1
#                        testfolder = testfile.rsplit(end, 1)[-1]            # gives        Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Pi\xf1a Colada Song).mp3
#                        testfolder = testfile.rsplit(end, 0)[0]             # gives          smb://Source Music/OSTs/Guardians of the Galaxy - Awesome Mix Vol. 1/Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Pi\xf1a Colada Song).mp3         
                        testfolder = testfile.rsplit(end, 1)[0] + "/"       # gives         smb://Source Music/OSTs/Guardians of the Galaxy - Awesome Mix Vol. 1/
                        
                        
#                       .rsplit('_', 1)[0]
                        print ('testfolder is %s'% testfolder)
                        contents = []
                        contents = xbmcvfs.listdir(testfolder)
                        print 'contents are:'
                        for r in contents:
                            print r
                        if v > 1:
                            try:
                                prevfile = playlist(v-1)
                                print ('prevfile is %s'% prevfile)
                                for p in contents:
                                    if p == prevfile:
                                        q = p + 1
                                        missing = contents[q]
                                        print ('missing file is %s'% missing)    
                            except:
                                print 'oops170'


                v = v + 1                    
            
            
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



#    xbmc.executebuiltin('Notification(Try, again)')



exit()


#quest = 'The Piña Colada Song'
#questunicode = unicode(quest, 'utf-8', errors='ignore')
#print ('quest is %s'% quest)
#print ('questunicode is %s'% questunicode)

s = 'Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Pi\xf1a Colada Song).mp3'
print ('s is %s'% s)
#sreal = str.encode(s)
#sreal = bytes.decode(s)

#print ('sreal is %s'% sreal)
h = []
h.append(s)
t = h[0]
print ('t is %s'% t)
# u = t.decode('iso-8859-1')
# u = t.decode('utf-8')
#u = unicode(t, 'Latin-1')
#print ('u is %s'% u)

v = 'Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Piña Colada Song).mp3'
print ('v is %s'% v)
j = []
j.append(v)
print ('j is %s'% j)
w = j[0]
print ('w is %s'% w)



print 'woop'
g = v + v
print ('g is %s'% g)
y = s + s
print ('y is %s'% y)



# get settings    
#json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "video.playcountminimumpercent"}, "id": 1 }')
#print 'json_query is:'
#print json_query

xbmc.executebuiltin('Notification(All, done)')


# returns:
# json_query is:
# {"id":1,"jsonrpc":"2.0","result":{"items":[{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-01 Stay With Me Baby.mp3","label":"1-01 Stay With Me Baby.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-02 All Day And All Of The Night.mp3","label":"1-02 All Day And All Of The Night.mp3","type":"song"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-03 Elenore.mp3","label":"1-03 Elenore.mp3","type":"song"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-04 Judy In Disguise (With Glasses).mp3","label":"1-04 Judy In Disguise (With Glasses).mp3","type":"song"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-05 Dancing In The Street (Single V.mp3","label":"1-05 Dancing In The Street (Single V.mp3","type":"song"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-06 Wouldn't It Be Nice.mp3","label":"1-06 Wouldn't It Be Nice.mp3","type":"song"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-07 Ooo Baby Baby.mp3","label":"1-07 Ooo Baby Baby.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-08 This Guy's In Love With You.mp3","label":"1-08 This Guy's In Love With You.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-09 Crimson And Clover.mp3","label":"1-09 Crimson And Clover.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-10 Hi Ho Silver Lining.mp3","label":"1-10 Hi Ho Silver Lining.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-11 I Can See For Miles.mp3","label":"1-11 I Can See For Miles.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-12 With A Girl Like You.mp3","label":"1-12 With A Girl Like You.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-13 The Letter.mp3","label":"1-13 The Letter.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-14 I'm Alive.mp3","label":"1-14 I'm Alive.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-15 Yesterday Man.mp3","label":"1-15 Yesterday Man.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-16 I've Been A Bad Bad Boy.mp3","label":"1-16 I've Been A Bad Bad Boy.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-17 Silence Is Golden.mp3","label":"1-17 Silence Is Golden.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-18 The End Of The World.mp3","label":"1-18 The End Of The World.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-01 Friday On My Mind.mp3","label":"2-01 Friday On My Mind.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-02 My Generation (Original Mono Ve.mp3","label":"2-02 My Generation (Original Mono Ve.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-03 I Feel Free.mp3","label":"2-03 I Feel Free.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-04 The Wind Cries Mary (Stereo Ver.mp3","label":"2-04 The Wind Cries Mary (Stereo Ver.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-05 A Whiter Shade Of Pale.mp3","label":"2-05 A Whiter Shade Of Pale.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-06 These Arms Of Mine.mp3","label":"2-06 These Arms Of Mine.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-07 Cleo's Mood.mp3","label":"2-07 Cleo's Mood.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-08 The Happening.mp3","label":"2-08 The Happening.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-09 She'd Rather Be With Me.mp3","label":"2-09 She'd Rather Be With Me.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-10 98.6.mp3","label":"2-10 98.6.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-11 Sunny Afternoon.mp3","label":"2-11 Sunny Afternoon.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-12 Father And Son.mp3","label":"2-12 Father And Son.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-13 Nights In White Satin (Single E.mp3","label":"2-13 Nights In White Satin (Single E.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-14 You Don't Have To Say You Love.mp3","label":"2-14 You Don't Have To Say You Love.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-15 Stay With Me (Baby).mp3","label":"2-15 Stay With Me (Baby).mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-16 Hang On Sloopy.mp3","label":"2-16 Hang On Sloopy.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-17 This Old Heart Of Mine (Is Weak.mp3","label":"2-17 This Old Heart Of Mine (Is Weak.mp3","type":"unknown"},{"file":"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-18 Let's Dance.mp3","label":"2-18 Let's Dance.mp3","type":"unknown"}],"limits":{"end":36,"start":0,"total":36}}}


# Error Type: <type 'exceptions.UnicodeEncodeError'>
# Error Contents: 'ascii' codec can't encode character u'\xf1' in position 2684: ordinal not in range(128)
# Traceback (most recent call last):
# File "E:\XBMC Stuff\Krypton nightly\portable_data\userdata\smashing\smashingfavourites\scripts\testscripts\test1.py", line 12, in <module>
# print json_query
# File "<string>", line 7, in write
# UnicodeEncodeError: 'ascii' codec can't encode character u'\xf1' in position 2684: ordinal not in range(128)


# files:
# [{u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-01 Stay With Me Baby.mp3', u'label': u'1-01 Stay With Me Baby.mp3'}, {u'type': u'song', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-02 All Day And All Of The Night.mp3', u'label': u'1-02 All Day And All Of The Night.mp3'}, {u'type': u'song', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-03 Elenore.mp3', u'label': u'1-03 Elenore.mp3'}, {u'type': u'song', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-04 Judy In Disguise (With Glasses).mp3', u'label': u'1-04 Judy In Disguise (With Glasses).mp3'}, {u'type': u'song', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-05 Dancing In The Street (Single V.mp3', u'label': u'1-05 Dancing In The Street (Single V.mp3'}, {u'type': u'song', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-06 Wouldn't It Be Nice.mp3", u'label': u"1-06 Wouldn't It Be Nice.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-07 Ooo Baby Baby.mp3', u'label': u'1-07 Ooo Baby Baby.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-08 This Guy's In Love With You.mp3", u'label': u"1-08 This Guy's In Love With You.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-09 Crimson And Clover.mp3', u'label': u'1-09 Crimson And Clover.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-10 Hi Ho Silver Lining.mp3', u'label': u'1-10 Hi Ho Silver Lining.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-11 I Can See For Miles.mp3', u'label': u'1-11 I Can See For Miles.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-12 With A Girl Like You.mp3', u'label': u'1-12 With A Girl Like You.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-13 The Letter.mp3', u'label': u'1-13 The Letter.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-14 I'm Alive.mp3", u'label': u"1-14 I'm Alive.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-15 Yesterday Man.mp3', u'label': u'1-15 Yesterday Man.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/1-16 I've Been A Bad Bad Boy.mp3", u'label': u"1-16 I've Been A Bad Bad Boy.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-17 Silence Is Golden.mp3', u'label': u'1-17 Silence Is Golden.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/1-18 The End Of The World.mp3', u'label': u'1-18 The End Of The World.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-01 Friday On My Mind.mp3', u'label': u'2-01 Friday On My Mind.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-02 My Generation (Original Mono Ve.mp3', u'label': u'2-02 My Generation (Original Mono Ve.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-03 I Feel Free.mp3', u'label': u'2-03 I Feel Free.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-04 The Wind Cries Mary (Stereo Ver.mp3', u'label': u'2-04 The Wind Cries Mary (Stereo Ver.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-05 A Whiter Shade Of Pale.mp3', u'label': u'2-05 A Whiter Shade Of Pale.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-06 These Arms Of Mine.mp3', u'label': u'2-06 These Arms Of Mine.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-07 Cleo's Mood.mp3", u'label': u"2-07 Cleo's Mood.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-08 The Happening.mp3', u'label': u'2-08 The Happening.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-09 She'd Rather Be With Me.mp3", u'label': u"2-09 She'd Rather Be With Me.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-10 98.6.mp3', u'label': u'2-10 98.6.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-11 Sunny Afternoon.mp3', u'label': u'2-11 Sunny Afternoon.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-12 Father And Son.mp3', u'label': u'2-12 Father And Son.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-13 Nights In White Satin (Single E.mp3', u'label': u'2-13 Nights In White Satin (Single E.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-14 You Don't Have To Say You Love.mp3", u'label': u"2-14 You Don't Have To Say You Love.mp3"}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-15 Stay With Me (Baby).mp3', u'label': u'2-15 Stay With Me (Baby).mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-16 Hang On Sloopy.mp3', u'label': u'2-16 Hang On Sloopy.mp3'}, {u'type': u'unknown', u'file': u'smb://Source Music/OSTs/The Boat That Rocked (2009)/2-17 This Old Heart Of Mine (Is Weak.mp3', u'label': u'2-17 This Old Heart Of Mine (Is Weak.mp3'}, {u'type': u'unknown', u'file': u"smb://Source Music/OSTs/The Boat That Rocked (2009)/2-18 Let's Dance.mp3", u'label': u"2-18 Let's Dance.mp3"}]

    
v = 'Piña'
print ('v is %s'% v)                                    # v is Piña
w = v.decode("latin").encode("utf-8")                   # w is PiÃ±a        want   Pi\xf1a
print ('w is %s'% w)
x = v.decode("latin-1").encode("utf-8")                 # x is PiÃ±a
print ('x is %s'% x)
y = v.decode("latin").encode("iso-8859-1")
print ('y is %s'% y)

d = 'Pi\xf1a'
e = d.decode("iso-8859-1").encode("latin-1")
print ('e is %s'% e)




