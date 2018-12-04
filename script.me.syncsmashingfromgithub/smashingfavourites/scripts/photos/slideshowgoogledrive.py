#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import os


USERDATA = xbmc.translatePath('special://masterprofile')
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")

print 'running slideshowgoogledrive.py'

if not os.path.isfile(ADVANCEDSETTINGS):
    xbmc.executebuiltin('Notification(Operation cancelled, No advancedsettings found)')
    exit()
   
    
lines = file(ADVANCEDSETTINGS, 'r').readlines()
num = len(lines)
print ('num is %d'% num)
c = 0
while c < num:
    test = lines[c].strip()
    if test == '<from>smb://Source GooglePhotos</from>':
        d = c + 1
        checkline = lines[d].strip()
        c = 1000
    else:
        c = c + 1
# lines.close()
if c < 1000:
    xbmc.executebuiltin('Notification(Operation cancelled, Path not found in advancedsettings)')
    exit()
start = '<to>'
finish = '</to>'
googlephotos = (checkline.split(start))[1].split(finish)[0]
googlephotos = googlephotos.strip()

# googlephotos = 'E:\\Google Drive\\Google Photos\\'

    
print ('googlephotos is %s'% googlephotos)


xbmc.executebuiltin('Slideshow(%s, notrandom)'% googlephotos)
xbmc.executebuiltin('Notification(Slideshow, started)')

exit()



   

