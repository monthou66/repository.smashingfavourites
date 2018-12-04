# -*- coding: utf-8 -*-
# get masterprofile
import xbmc
import os
import subprocess

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"     
# Do it		

Input = subprocess("blkid /dev/sdc")
# Input = subprocess.getoutput("blkid /dev/sdc")
print(Input)	
printstar()
print "test9.py has just been started"
print(Input)
#print ('testy = %s' % testy)
printstar()
# xbmc.executebuiltin('Notification(test4.py, started)')
