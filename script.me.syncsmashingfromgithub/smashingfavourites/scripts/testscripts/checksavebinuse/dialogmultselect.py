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
CHOICES = []	
CHOOSE = xbmcgui.Dialog().multiselect("Options", OPTIONS)

number = len(CHOOSE)	
c=0
while c < number:
    d = str(c)
    e = c + 1
    f = str(e)
    choice = OPTIONS[c]
    CHOICES.append(choice)
    print choice
#    ('choice%s' % f) = CHOOSE[c]
#    f = ('choice%s' % e)
#    ('option%s' % e) = OPTIONS[f]
    c = c + 1
	

printstar()
print ('OPTIONS = %s' % OPTIONS)
print CHOOSE
print number
print CHOICES
#print choice1
#print choice2
#print option1
#print option2
#print ("Choice = %s" % CHOICE)
printstar()
xbmc.executebuiltin('Notification(test4.py, started)')