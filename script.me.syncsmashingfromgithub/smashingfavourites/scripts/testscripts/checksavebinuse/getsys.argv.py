# -*- coding: utf-8 -*-

import xbmc


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

d = len(sys.argv)
e = sys.argv[0]

opt = 'none'
bla = 'none'
if d > 1:
    opt = sys.argv[1]
if d > 2:
   bla = sys.argv[2]
	
printstar()
print "test3.py has just been started"
print ('len(sys.argv) = %d' % d)
print ('sys.argv[0] = %s' % e)
print ('opt = %s' % opt)
print ('bla = %s' % bla)
printstar()
xbmc.executebuiltin('Notification(test3.py, started)')

exit()

# start this with:
# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
xbmc.executebuiltin('XBMC.RunScript(special://masterprofile/smashing/smashingfavourites/scripts/testscripts/test3.py, one, two)')	
printstar()
print "test4.py has just been started"
printstar()

	