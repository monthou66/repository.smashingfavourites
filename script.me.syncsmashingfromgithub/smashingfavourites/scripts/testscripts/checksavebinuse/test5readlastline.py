# -*- coding: utf-8 -*-
import xbmc
import os
# read last line of a file

favouritesfile = '/storage/.kodi/userdata/favourites/xonfluence/favourites.xml'

lines = file(favouritesfile, 'r').readlines()
print "***********************************************************************************"	
print "**********************************************************************************"
subset = lines[-1]
print subset
if subset=='xonfluence':
   print 'yay'
else:
    print 'boo'
print "***********************************************************************************"	
print "**********************************************************************************"
