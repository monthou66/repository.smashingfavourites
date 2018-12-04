# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os

# To show up in log:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def printworking():
    print "smashingxonf is doing stuff."
	
def printproblem():
    print "There is a problem with smashingxonfluence."
	
def printabandon():
    print "Script ended by user."
	
def printnorestore():
    print "No restore performed."
	
def printnobackup():
    print "No backup performed."
	
def printbackup():
    print "Xonfluence has been backed up."
	
def backupdone():
    xbmc.executebuiltin('Notification(Xonfluence has been, backed up)')
	
# Try generate list
FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/backups/")
LIST = []
LIST = os.listdir(FOLDER)
length = len(LIST)
backups = []
c = 0
while c < length:
    check = LIST[c]
    checkpath = os.path.join(FOLDER, check)
    if os.path.isdir(checkpath):
        backups.append(check)
    c = c + 1

ZERO = LIST [0]
ONE = LIST [1]

print ('LIST is %s'% LIST)
print ('ZERO is %s'% ZERO)
print ('ONE is %s'% ONE)
print ('length is %s'% length)
print ('backups are %s'% backups)
CHOOSE = xbmcgui.Dialog().select("Choose Backup to restore", backups)

print ("Choice is %d" % CHOOSE)

CHOICE = backups[CHOOSE]
print ("Backup to restore is %s" % CHOICE)
