# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "test1.py has just been started"
printstar()
xbmc.executebuiltin('Notification(test1.py, started)')

# original:
#    <favourite name="Music">ActivateWindow(10502,&quot;smb://Source Music/&quot;,return)</favourite>

# now:
#    <favourite name="testrunfav">RunScript(special://masterprofile/smashing/smashingfavourites/scripts/testscripts/testfav.py)</favourite>

# works:
xbmc.executebuiltin('ActivateWindow(10502,"smb://Source Music/",return)')

# format is:
#    <favourite name="NAME" thumb="THUMB">RunScript(SCRIPT)</favourite>



