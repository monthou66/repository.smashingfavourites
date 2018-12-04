# -*- coding: utf-8 -*-
import xbmc
import os
# http://stackoverflow.com/questions/4260116/find-size-and-free-space-of-the-filesystem-containing-a-given-file
# Get partition free space

target = '/storage/.kodi/userdata/favourites.xml'
def freespace(target):
    "Get the free space of the filesystem containing pathname"
    stat= os.statvfs(target)
    # use f_bfree for superuser, or f_bavail if filesystem
    # has reserved space for superuser
    return stat.f_bfree*stat.f_bsize

print "***********************************************************************************"	
print "**********************************************************************************"
print "Target size: %d" % freespace(target)
print "***********************************************************************************"	
print "**********************************************************************************"