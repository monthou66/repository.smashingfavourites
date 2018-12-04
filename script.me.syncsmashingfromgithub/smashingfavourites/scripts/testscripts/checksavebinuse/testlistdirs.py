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
FOLDER = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/backups/skins/xonfluence/")

def listdirs(FOLDER):
    global LIST
    LIST = [
        d for d in (os.path.join(FOLDER, d1) for d1 in os.listdir(FOLDER))
        if os.path.isdir(d)
    ]

listdirs(FOLDER)

print "LIST is %s" % LIST