# -*- coding: utf-8 -*-

import xbmc
import xbmcgui


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

OPTIONS = ['Enable debugging', 'Disable debugging', 'Check current advanced settings', 'Choose a new advanced settings from a list', 'choose options for advanced settings']
#OPTIONS[0] = 'Enable debugging'
#OPTIONS[1] = 'Disable debugging'
#OPTIONS[2] = 'Check current advanced settings'
#OPTIONS[3] = 'Choose a new advanced settings from a list'
#OPTIONS[4] = 'choose options for advanced settings'
	
CHOOSE = xbmcgui.Dialog().select("Options", OPTIONS)
CHOICE = OPTIONS[CHOOSE]

printstar()
print ('OPTIONS = %s' % OPTIONS)
print ('CHOOSE = %d' % CHOOSE)
print ('CHOICE = %s' % CHOICE)
printstar()
xbmc.executebuiltin('Notification(test4.py, started)')