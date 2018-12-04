#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import os
import sys

USERDATA = xbmc.translatePath('special://masterprofile')
functions = os.path.join(USERDATA, "smashing", "smashingfavourites", "scripts", "functions")

sys.path.insert(0, functions)

# from genericstartscript import printstar

genericstartscript.printstar()
print "test4.py has just been started"
genericstartscript.printstar()
print 'test'
genericstartscript.printstar()