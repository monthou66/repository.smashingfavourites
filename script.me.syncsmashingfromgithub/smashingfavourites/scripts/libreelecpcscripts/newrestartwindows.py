# -*- coding: utf-8 -*-
# restartintosomethingelse.py
# restart windows or a different libreelec version from libreelec
import xbmc
import os
import shutil
import sys

newstuff = sys.argv[1]
print ('Libreelec will reboot into %s'% newstuff)
# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "libreelecpcscripts")
flashrw = os.path.join(folder, "makeflashrw.sh")
flashro = os.path.join(folder, "makeflashro.sh")
libreelec = os.path.join("/flash", "libreelec.txt")
menulst = os.path.join("/flash", "menu.lst")
SYSTEM = os.path.join("/flash", "SYSTEM")
KERNEL = os.path.join("/flash", "KERNEL")
source = os.path.join("/flash", "stuff", "menus", newstuff)
NEWSYSTEM = os.path.join(source, "SYSTEM")
NEWKERNEL = os.path.join(source, "KERNEL")
newlibreelec = os.path.join(source, "libreelec.txt")
newmenulst = os.path.join(source, "menu.lst")
newlibretext = os.path.join(source, "%s.txt"% newstuff)
# Read librelec
file = open(libreelec, 'r')
libreversion = file.read()
# print ('libreversion is %s'% libreversion)
# check libreversion text file exists
libretext = os.path.join("/flash", "%s.txt"% libreversion)
oldstuff = os.path.join("/flash", "stuff", "menus", libreversion)
OLDSYSTEM = os.path.join(oldstuff, "SYSTEM")
OLDKERNEL = os.path.join(oldstuff, "KERNEL")
# check all files are present
if not os.path.exists(libreelec):
elif not os.path.exists(libretext):
elif not os.path.exists(menulst):

    xbmc.executebuiltin('Notification(noway, jose)')
    print 'Problem - can\'t find libreversion.txt - sort it out!'
    exit()
# xbmc.executebuiltin('Notification(ohyeah, jose)')




exit()
# Do it		
os.system('sh %s post' % flashrw)
xbmc.sleep(300)
if os.path.exists(libreelec):
    os.remove(libreelec)
if os.path.exists(menulst):
    os.remove(menulst)
shutil.copy(newlibreelec, libreelec)
shutil.copy(newmenulst, menulst)
os.system('sh %s post' % flashro)
xbmc.sleep(300)

xbmc.executebuiltin('Reboot')

 
# Drink beer