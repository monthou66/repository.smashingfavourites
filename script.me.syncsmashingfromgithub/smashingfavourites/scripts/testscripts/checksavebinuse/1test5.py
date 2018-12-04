# -*- coding: utf-8 -*-

import xbmc

def star():
    print "***************************************************************************************"
    print "****************************************************************************************"

f = open('/storage/.kodi/userdata/favourites/scripts/kodilogtemp.txt')
lines = f.readlines()
f.close()

star()
print lines[0]
print lines[1]
print lines[2]
star()
exit()

