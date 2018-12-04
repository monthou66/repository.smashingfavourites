#!/usr/bin/python
# -*- coding: utf-8 -*-

#import xbmc
#import os
#import sys

import xbmc
import xbmcgui
import os
import shutil
import sys
from time import gmtime, strftime

USERDATA = xbmc.translatePath('special://masterprofile')
functions = os.path.join(USERDATA, "smashing", "smashingfavourites", "scripts", "functions")
startscript = os.path.join(functions, "genericstartscript")
#sys.path.insert(0, scripts)
# from genericstartscript import printstar()
from ..genericstartscript import printstar

printstar()
print "test3.py has just been started"
printstar()
print 'test'
printstar()

