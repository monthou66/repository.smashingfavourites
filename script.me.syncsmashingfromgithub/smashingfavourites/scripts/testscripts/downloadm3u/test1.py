# -*- coding: utf-8 -*-
# downloadlogos.py
import xbmc
import urllib
import os
import shutil

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

thisaddon = sys.argv[0]	
printstar()
print ('%s has started'% thisaddon)
printstar()
xbmc.executebuiltin('Notification(%s, started)'% thisaddon)


# url = "http://fabiptv.com/getlogos/logos/ESPNews.png"
# head, tail = os.path.split(url)
# print ('head is %s'% head)
# print ('tail is %s'% tail)
# exit()

# url = "http://fabiptv.com/getlogos/logos/ESPNews.png"
# fname = "E:\ESPNews.png"
# urllib.urlretrieve( url, fname )
# xbmc.sleep(2000)
# xbmc.executebuiltin('Notification(All, done)')
# exit()






# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
IPTVFOLDER = os.path.join(SMASHINGTEMP, "iptv")
MERGED = os.path.join(IPTVFOLDER, "merged.m3u")
XMLTV = os.path.join(IPTVFOLDER, "test.xml")
NEWMERGED = os.path.join(IPTVFOLDER, "newmerged.m3u")
LOGOSFOLDER =  os.path.join(IPTVFOLDER, "logos")
IPTVFILE = urllib.URLopener()

# open merged.m3u, search for string - (logo="http://..xyzpng")
# check if 'LOGOSFOLDER/xyz.png' is file.  If not download it
# change path in .m3u to 'LOGOSFOLDER/xyz.png'

if os.path.isfile(MERGED):
    with open(MERGED) as foo:
        length = len(foo.readlines())
    lines = file(MERGED, 'r').readlines()
    w = 1
    while w < length:
        checkline = lines[w]
		
        if 'logo="http' in checkline:	
            start = 'logo="'		
            end = '" group-title'		
            LINK = checkline[checkline.find(start)+len(start):checkline.rfind(end)]
            head, checklogo = os.path.split(LINK)

# url = "http://fabiptv.com/getlogos/logos/ESPNews.png"
# head, tail = os.path.split(url)
# print ('head is %s'% head)
# print ('tail is %s'% tail)


            # check 'checklogo' is a valid filename (ends with .jpg / .png) - otherwise extract filename
            if not checklogo[-3:] == 'png':
                printstar()
                print 'checklogo does not end in png'
                if not checklogo[-3:] == 'jpg':
                    if not checklogo[-3:] == 'jpeg':
                        # slice
                        if 'png' in checklogo:
                            ext = 'png'
                        elif 'jpg' in checklogo:
                            ext = 'jpg'
                        elif 'jpeg' in checklogo:
                            ext = 'jpeg'
                        else:
                            printstar()
                            print ('Cannot find valid extension in %s'% checklogo)
                            checklogo = 'invalid'
                        if not checklogo == 'invalid':
                            checklogo = checklogo.split(ext, 1)[0] + ext
#s = s.split('.zip', 1)[0] + '.zip'						


#            print ('checklogo is %s'% checklogo)
#            printstar()
#            exit()

		
#        if 'logo="http://fabiptv.com/getlogos/logos/' in checkline:
#            start = 'logo="http://fabiptv.com/getlogos/logos/'
#            end = '" group-title'
#            checklogo = checkline[checkline.find(start)+len(start):checkline.rfind(end)]
#            print ('checklogo is %s'% checklogo)
            if not checklogo == 'invalid':
                LOCALLOGO =  os.path.join(LOGOSFOLDER, checklogo)
                if not os.path.isfile(LOCALLOGO):
#                    LINK = ('http://fabiptv.com/getlogos/logos/%s'% checklogo)
# check logo exists
                    if urllib.urlopen(LINK).code == 200:
                        IPTVFILE.retrieve(LINK, LOCALLOGO)
#                        xbmc.sleep(300)
                        print ('LINK is %s'% LINK)
                        print ('LOCALLOGO is %s'% LOCALLOGO)
                    else:
                        printstar()
                        print ('problem with %s'% LINK)
        w = w + 2

# exit()

# edit file to point at local logos if present
fin = open(MERGED)
fout = open(NEWMERGED, "w+")
for line in fin:
    if 'logo="http' in line:
#        fout.write(line)
        # get full path to logo, get filename, check if file exists in local folder - if it does edit line
        start = 'logo="'		
        end = '" group-title'		
        LINK = line[line.find(start)+len(start):line.rfind(end)]
        head, checklogo = os.path.split(LINK)

        if not checklogo[-3:] == 'png':
            printstar()
            print 'checklogo does not end in png'
            if not checklogo[-3:] == 'jpg':
                if not checklogo[-3:] == 'jpeg':
                    # slice
                    if 'png' in checklogo:
                        ext = 'png'
                    elif 'jpg' in checklogo:
                        ext = 'jpg'
                    elif 'jpeg' in checklogo:
                        ext = 'jpeg'
                    else:
                        printstar()
                        print ('Cannot find valid extension in %s'% checklogo)
                        checklogo = 'invalid'
                    if not checklogo == 'invalid':
                        checklogo = checklogo.split(ext, 1)[0] + ext		
        if not checklogo == 'invalid':
            LOCALLOGO =  os.path.join(LOGOSFOLDER, checklogo)
            if os.path.isfile(LOCALLOGO):
# Messing
                LOCALLOGO = 'http://rubbish.com/getlogos/logos/rubbish.png'
                line = line.replace(LINK, LOCALLOGO)				
    fout.write(line)		
		
		
		
fin.close()
fout.close()
os.remove(MERGED)
os.rename(NEWMERGED, MERGED)

# download xmltv
# special://masterprofile/smashing/smashingfavourites/miscfiles/iptv/test.xml
# http://stream.fabiptv.com:25461/xmltv.php?username=oqrfxtzg&amp;password=m7q38iA3wE
# http://stream.fabiptv.com:25461/xmltv.php?username=oqrfxtzg&password=m7q38iA3wE
# http://fabiptv.co.uk:4545/xmltv.php?username=oqrfxtzg&password=m7q38iA3wE

EPGURL = "http://stream.fabiptv.com:25461/xmltv.php?username=oqrfxtzg&password=m7q38iA3wE"
if urllib.urlopen(EPGURL).code == 200:
    IPTVFILE.retrieve(EPGURL, XMLTV)




xbmc.executebuiltin('Notification(%s, done)'% thisaddon)
exit()

infile = "messy_data_file.txt"
outfile = "cleaned_file.txt"

delete_list = ["word_1", "word_2", "word_n"]
fin = open(infile)
fout = open(outfile, "w+")
for line in fin:
    for word in delete_list:
        line = line.replace(word, "")
    fout.write(line)
fin.close()
fout.close()











start = 'asdf=5;'
end = '123jasd'
s = 'asdf=5;iwantthis123jasd'
print s[s.find(start)+len(start):s.rfind(end)]




# checking age of last merged file.
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
IPTVFOLDER = os.path.join(SMASHINGTEMP, "iptv")
DOWNLOADFIRSTFOLDER = os.path.join(IPTVFOLDER, "downloadfirst")
FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, 'fabiptv.m3u')
TIMEFIRSTFILE = os.path.getmtime(FIRSTFILE)
TEMP = os.path.join(DOWNLOADFIRSTFOLDER, 'temp.txt')
TEMPFILE = open(TEMP, 'w')
TIMETEMPFILE = os.path.getmtime(TEMP)
AGEFIRST = TIMETEMPFILE - TIMEFIRSTFILE

print ('FIRSTFILE is %d seconds old'% AGEFIRST)
printstar()
exit()


# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
IPTVFOLDER = os.path.join(SMASHINGTEMP, "iptv")
SETTINGS = os.path.join(IPTVFOLDER, "settings.txt")
DOWNLOADFIRSTFOLDER = os.path.join(IPTVFOLDER, "downloadfirst")
# FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, 'fabiptv.m3u')
DOWNLOADRESTFOLDER = os.path.join(IPTVFOLDER, "downloadmore")
OLDFOLDER = os.path.join(IPTVFOLDER, "oldfiles")
OLDFILE = os.path.join(OLDFOLDER, 'fabiptv.m3u')
IPTVFILE = urllib.URLopener()
APPENDFOLDER =  os.path.join(IPTVFOLDER, "appendfiles")
# uksports = os.path.join(SMASHINGTEMP, "iptv", "fabiptv", "uksports.m3u")
out = os.path.join(IPTVFOLDER, "merged.m3u")
oldout = os.path.join(OLDFOLDER, "merged.m3u")

def mergefiles():
    global USERDATA, SMASHINGFAVOURITES, IPTVFOLDER, DOWNLOADFIRSTFOLDER, FIRSTFILE, DOWNLOADRESTFOLDER, OLDFOLDER, OLDFILE
    global IPTVFILE, APPENDFOLDER, out, oldout
# Delete the merged.m3u from OLDFOLDER (oldout) and move merged.m3u from IPTVFOLDER in to replace it (out).
    if os.path.isfile(oldout):
        os.remove(oldout)	
    if os.path.isfile(out):
        os.rename(out, oldout)
        print 'merged.m3u has been moved'
    else:
        print 'There was no merged.m3u file in place.'
# read first downloaded .m3u into merged
    f = open(FIRSTFILE, 'r')
    text = f.read()
    f.close()
    with open(out, "a") as myfile:
        myfile.write(text)
# read any other downloaded .m3u files into merged
    downrest = []
    downrest = os.listdir(DOWNLOADRESTFOLDER)
    total = len(downrest)
    if total > 0:
        for k in downrest:
            m3ufile = os.path.join(DOWNLOADRESTFOLDER, k)
            f = open(m3ufile, 'r')
            text = f.read()
            f.close()
            with open(out, "a") as myfile:
                myfile.write(text.replace('#EXTM3U#','').replace('#EXTM3U',''))
# read any local .m3u files into merged				
    appendrest = []
    appendrest = os.listdir(APPENDFOLDER)
    total = len(appendrest)
    if total > 0:
        for k in appendrest:
            m3ufile = os.path.join(APPENDFOLDER, k)
            f = open(m3ufile, 'r')
            text = f.read()
            f.close()
            with open(out, "a") as myfile:
                myfile.write(text.replace('#EXTM3U#','').replace('#EXTM3U',''))				
				
				
				
    xbmc.executebuiltin('Notification(m3us have been, merged)')

# Get on with it.
	
# empty OLDFOLDER
# Move files from DOWNLOADFIRSTFOLDER and DOWNLOADRESTFOLDER into OLDFOLDER

fileList = os.listdir(OLDFOLDER)
for fileName in fileList:
    print ('File to delete from old folder is %s'% fileName)
    DELETEME = os.path.join(OLDFOLDER, fileName)
    os.remove(DELETEME)

fileList = os.listdir(DOWNLOADFIRSTFOLDER)
for fileName in fileList:
    print ('File to move from downloadfirstfolder to old folder is %s'% fileName)
    MOVEME = os.path.join(DOWNLOADFIRSTFOLDER, fileName)
    MOVED = os.path.join(OLDFOLDER, fileName)
    os.rename(MOVEME, MOVED)		
		
fileList = os.listdir(DOWNLOADRESTFOLDER)
for fileName in fileList:
    print ('File to move from downloadrestfolder to old folder is %s'% fileName)
    MOVEME = os.path.join(DOWNLOADRESTFOLDER, fileName)
    MOVED = os.path.join(OLDFOLDER, fileName)
    os.rename(MOVEME, MOVED)

# Download m3us	
# read SETTINGS to get name and url for each .m3u file
# line 1 = name of FIRSTFILE, line 2 = url; line 3 = name of next download etc
if os.path.isfile(SETTINGS):
# count lines in file
    with open(SETTINGS) as foo:
        length = len(foo.readlines())
    links = length/2
    print ('length is %d lines'% length)
    print ('There are %d files to download'% links)
    lines = file(SETTINGS, 'r').readlines()
    FIRSTNAME = lines[0].rstrip()
    FIRSTFILE = os.path.join(DOWNLOADFIRSTFOLDER, FIRSTNAME)
    FIRSTLINK = lines[1].rstrip()
       		
    print ('FIRSTFILE is %s'% FIRSTFILE)
    print ('FIRSTLINK is %s'% FIRSTLINK)
    IPTVFILE.retrieve(FIRSTLINK, FIRSTFILE)	
    xbmc.sleep(1000)
# check if there are more links in SETTINGS
    if links > 1:
        p = 2
        while p < length:
            NEXTNAME = lines[p].rstrip()
            NEXTFILE = os.path.join(DOWNLOADRESTFOLDER, NEXTNAME)
            p = p + 1
            NEXTLINK = lines[1].rstrip()
            p = p + 1	
            IPTVFILE.retrieve(NEXTLINK, NEXTFILE)
            xbmc.sleep(1000)
else:		
    printstar()
    print "No valid settings file detected in iptvfolder"
    printstar()
    xbmc.executebuiltin('Notification(No valid settings file, in iptvfolder)')	
	
print 'check 3'
if os.path.exists(FIRSTFILE):
    xbmc.executebuiltin('Notification(Way, hey)')
else:
    xbmc.executebuiltin('Notification(Boo, hoo)')

mergefiles()
	








