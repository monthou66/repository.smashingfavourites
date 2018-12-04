# -*- coding: utf-8 -*-

import xbmc

def star():
    print "***************************************************************************************"
    print "****************************************************************************************"

f = open('/storage/.kodi/userdata/favourites/scripts/kodilogtemp.txt')
lines = f.readlines()
f.close()

# get lenth of text file (how many lines)
length = len(lines)
k = str(length)

star()
print lines[0]
print lines[1]
print lines[2]
print ('There are %s lines.' % k)
star()
exit()

    #    print ('Unable to decrypt signature, key length %d not supported; retrying might work' % (len(s)))