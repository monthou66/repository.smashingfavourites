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

LIST = os.listdir(FOLDER)

length = len(LIST)
ZERO = LIST [0]
ONE = LIST [1]

print LIST
print ZERO
print ONE
print length
CHOOSE = xbmcgui.Dialog().select("Choose Backup to restore", LIST)

print ("Choice is %d" % CHOOSE)

CHOICE = LIST [CHOOSE]
print ("Backup to restore is %s" % CHOICE)
