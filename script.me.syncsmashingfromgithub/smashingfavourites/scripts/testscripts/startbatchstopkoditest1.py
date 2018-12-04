#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import os
import subprocess
from subprocess import Popen

print 'running test.py'
USERDATA = xbmc.translatePath('special://masterprofile')
batchfolder = os.path.join(USERDATA, 'batch')
batchfile = os.path.join(batchfolder, 'test.bat')
assert os.path.isdir(batchfolder)
os.chdir(batchfolder)
subprocess.Popen('test.bat', close_fds=True,  shell=True)
xbmc.executebuiltin('Notification(Stopping, kodi)')
xbmc.sleep(1000)
xbmc.executebuiltin('Quit')
exit()