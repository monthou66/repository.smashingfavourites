# -*- coding: utf-8 -*-
# teststartbat
import xbmc
import os
import subprocess
from subprocess import Popen

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"


USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")	
batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch")
batchfile = os.path.join(batchfolder, "test.bat")	
	
	
def startbat():

#    subprocess.Popen('C:\test.bat')
    subprocess.Popen('E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch\test.bat')

#    p = subprocess.Popen(r'start cmd /c C:\test.bat', shell=True)

#    p = subprocess.Popen(r'start cmd /c E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch\test.bat', shell=True)
#    p.wait()
	
#    p = Popen(batchfile, cwd=r"E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch\test.bat")	
#    p = Popen(batchfile, batchfolder)
#    stdout, stderr = p.communicate()



startbat()	
printstar()
print "teststartbat.py has just been started"
printstar()
xbmc.executebuiltin('Notification(teststartbat.py, started)')