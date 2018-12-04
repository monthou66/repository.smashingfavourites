#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc


xbmc.executebuiltin("System.LogOff")
xbmc.sleep(300)
xbmc.executebuiltin("LoadProfile(Master user)")
