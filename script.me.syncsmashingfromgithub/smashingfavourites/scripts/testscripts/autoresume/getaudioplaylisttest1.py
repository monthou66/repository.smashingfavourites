#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import json


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
        
listfiles = []
ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Playlist.GetItems", "params":{"playlistid":0,"properties":["file"]} }'))
files = ret['result']['items']
num = len(files)
print ('num = %d'% num)
c = 0
while c < num:
    f = files[c]
#    printstar()
#    print f
    fstring = str(f)
#    fstring = unicode(fstring, 'utf-8', errors='ignore')
    if '\\' in fstring:
        errornot()
#    print fstring
    start = "file': u'"
    end = "', u'label':"
    try:    
        test = (fstring.split(start))[1].split(end)[0]
    except:
        try:
            start = "file': u\""
            end = "\", u'label':"
            test = (fstring.split(start))[1].split(end)[0]
        except:        
            test = 'errored out'
    listfiles.append(test)
#  group = (gstring.split(start))[1].split(end)[0]
#    file = (fstring.split(start))[1]
    print test
    c = c + 1
    
playlist = 'music_-|-_' + '_-|-_'.join([x for x in listfiles]) 

print 'files:'
print files
print 'listfiles:'
print listfiles
print 'playlist:'
print playlist

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
json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "video.playcountminimumpercent"}, "id": 1 }')
print 'json_query is:'
print json_query

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






