#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import os
import shutil

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
SMASHINGSOURCE = os.path.join(USERDATA, "smashingsource")

print 'running test1.py'

if not os.path.isfile(ADVANCEDSETTINGS):
    exit()
if not os.path.isdir(SMASHINGSOURCE):
    os.mkdir(SMASHINGSOURCE)    
    
lines = file(ADVANCEDSETTINGS, 'r').readlines()
num = len(lines)
print ('num is %d'% num)
c = 0
while c < num:
    test = lines[c].strip()
    if test == '<from>smb://Source smashing</from>':
        d = c + 1
        checkline = lines[d].strip()
        c = 1000
    else:
        c = c + 1
# lines.close()
if c < 1000:
    exit()
start = '<to>'
finish = '</to>'
SAVEDSMASHINGFAVOURITES = (checkline.split(start))[1].split(finish)[0]
SAVEDSMASHINGFAVOURITES = SAVEDSMASHING.strip()

sourcesmashingfavourites = os.path.join(SAVEDSMASHINGFAVOURITES, "smashing", "smashingfavourites")
destsmashingfavourites = os.path.join(SMASHINGSOURCE, "smashingfavouritescopy")
    
print ('sourcesmashingfavourites is %s'% sourcesmashingfavourites)
print ('destsmashingfavourites is %s'% destsmashingfavourites)

if os.path.exists(destsmashingfavourites):
    shutil.rmtree(destsmashingfavourites)
    xbmc.sleep(300)
shutil.copytree(sourcesmashingfavourites, destsmashingfavourites)

sourcesmashingartwork = os.path.join(USERDATA, "smashing", "smashingartwork")
destsmashingartwork = os.path.join(SMASHINGSOURCE, "smashingartworkcopy")
    
print ('sourcesmashingartwork is %s'% sourcesmashingartwork)
print ('destsmashingartwork is %s'% destsmashingartwork)


if os.path.exists(destsmashingartwork):
    shutil.rmtree(destsmashingartwork)
    xbmc.sleep(300)
shutil.copytree(sourcesmashingartwork, destsmashingartwork)





xbmc.executebuiltin('Notification(All, done)')

exit()



   

