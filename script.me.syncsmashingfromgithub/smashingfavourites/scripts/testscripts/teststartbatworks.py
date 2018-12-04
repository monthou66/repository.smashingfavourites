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

#    inkscape_dir=r"C:\Program Files (x86)\Inkscape"
    batch_dir=r"E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch"
    assert os.path.isdir(batch_dir)
    os.chdir(batch_dir)
#    subprocess.Popen(['test.bat',"-f",fname,"-e",fname_png])
    subprocess.Popen('test.bat')


#    app = 'test.bat'
#    appPath = os.path.join(batchfolder, app)

#    commandLine = [app, 'arg1', 'arg2']
#    process = subprocess.Popen(commandLine, executable=appPath)



startbat()	
printstar()
print "teststartbat.py has just been started"
printstar()
xbmc.executebuiltin('Notification(teststartbat.py, started)')