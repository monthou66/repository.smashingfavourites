# -*- coding: utf-8 -*-
# opens tv channel or guide groups via smashingfavourites and / or keymap.
import os
import os.path
import xbmc
import sys

#define terms... c = count, f = 1 (value) if channels, f=2 (value) if guides, g = group number (value)
a = sys.argv[1]
b = sys.argv[2]
c = 2
d = str(c)
f = int(a)
g = int(b)
h = f + g
j = str(h)

# open channel or guide windows
if f == 1:
	xbmc.executebuiltin('ActivateWindow(TVChannels)')
elif f == 2: 
	xbmc.executebuiltin('ActivateWindow(TVGuide)')
else:
	xbmc.executebuiltin('Notification(Check, smashingtv)'); exit
	
xbmc.executebuiltin('SendClick(28)')
xbmc.executebuiltin( "XBMC.Action(FirstPage)" )

# loop move down to correct group (if necessary)
if g > 1:
	while (c <= g):	
		c = c + 1
		xbmc.executebuiltin( "XBMC.Action(Down)" )

# open group if not using 'choose' option.		
if g >=1:		
	xbmc.executebuiltin( "XBMC.Action(Select)" )
	xbmc.executebuiltin( "XBMC.Action(Right)" )
	xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )
else:
	exit	