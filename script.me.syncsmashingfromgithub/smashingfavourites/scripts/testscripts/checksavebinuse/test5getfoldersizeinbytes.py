# -*- coding: utf-8 -*-
import xbmc
import os
# http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
# Get source directory size

source = '/storage/.kodi'

def FolderSize(source):
    total_size = os.path.getsize(source)
    for item in os.listdir(source):
        itempath = os.path.join(source, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += FolderSize(itempath)
    return total_size

print "***********************************************************************************"	
print "**********************************************************************************"
print "Source size: %d" % FolderSize(source)
print "***********************************************************************************"	
print "**********************************************************************************"