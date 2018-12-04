# -*- coding: utf-8 -*-

import xbmc

# Get inputs via sys.argv[1,2]
# backup or restore?
# Target and Source?
# Confirm target and source with ok check
# if not either finish (easy) or ask for path
# make sure both exist = if target not exist mkdir
# write paths (and options, eg make flash writeable, stop kodi????) to text file/s.
# start rsync (or rename delete folders if required?)




# http://stackoverflow.com/questions/4260116/find-size-and-free-space-of-the-filesystem-containing-a-given-file
# Get partition free space
def get_fs_freespace(pathname):
    "Get the free space of the filesystem containing pathname"
    stat= os.statvfs(pathname)
    # use f_bfree for superuser, or f_bavail if filesystem
    # has reserved space for superuser
    return stat.f_bfree*stat.f_bsize
	
print "Target size: " + str(get_fs_freespace("."))	

# http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
# Get source directory size
def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

print "Source size: " + str(getFolderSize("."))

if total_size > stat.f_bfree*stat.f_bsize:
    run away










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