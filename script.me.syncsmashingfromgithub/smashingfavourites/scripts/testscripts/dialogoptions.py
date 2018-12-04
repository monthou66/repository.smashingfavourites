# -*- coding: utf-8 -*-

import xbmc
import xbmcgui


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

OPTIONS = ['one', 'two', 'three', 'four', 'five']
OPTIONS[0] = 'test'
OPTIONS[1] = 'backup databases'
OPTIONS[2] = 'remove old databases'
OPTIONS[3] = 'toggle debug logging'
OPTIONS[4] = 'choose new advanced settings'
	
CHOOSE = xbmcgui.Dialog().select("Options", OPTIONS)
CHOICE = OPTIONS[CHOOSE]
	
	
	

printstar()
print ('OPTIONS = %s' % OPTIONS)
print ('CHOOSE = %d' % CHOOSE)
print ("Choice = %s" % CHOICE)
printstar()
xbmc.executebuiltin('Notification(test4.py, started)')