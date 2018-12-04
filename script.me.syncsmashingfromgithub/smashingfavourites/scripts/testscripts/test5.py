# -*- coding: utf-8 -*-

import xbmc
import os
import subprocess
from subprocess import Popen
# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# start batch
batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch", "hide")
batchfile = os.path.join(batchfolder, "test.bat")
assert os.path.isdir(batchfolder)
os.chdir(batchfolder)
# Visible    subprocess.Popen('test.bat')
# Invisible        subprocess.Popen('test.bat',  shell=True)

subprocess.Popen('test.bat', close_fds=True)

#subprocess.Popen('test.bat')

#        xbmc.sleep(1000)
#        xbmc.executebuiltin('Quit')



#os.system("D:/xxx1/xxx2XMLnew/otr.bat ")

#os.system("E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch\hide\test.bat ")

#os.system(r"E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch\hide\test.bat ")

#os.system("E:\\XBMC Stuff\\kryptonmess\\portable_data\\userdata\\smashingfavourites\\scripts\\batch\\hide\\test.bat ")

#os.system("E:/XBMC Stuff/kryptonmess/portable_data/userdata/smashing/smashingfavourites/scripts/batch/hide/test.bat ")

#E:\XBMC Stuff\kryptonmess\portable_data\userdata\smashingfavourites\scripts\batch\hide



	
printstar()
print "test5.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')