# -*- coding: utf-8 -*-
# test edit batch
import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

USERDATA = xbmc.translatePath('special://masterprofile')
TEST = os.path.join(USERDATA, "smashing", "smashingfavourites")
# need to define:
THUMBNAILSFOLDER = os.path.join(TEST, "Thumbnails")
oldthumbs = os.path.join(TEST, "OldThumbnails")
newthumbs = os.path.join(TEST, "OldThumbnails")
savevideodbfile = os.path.join(TEST, "savevideodbfile")
savetexturesdbfile = os.path.join(TEST, "savetexturesdbfile")
newdb = os.path.join(TEST, "newdb")
DATABASEFOLDER os.path.join(TEST, "Database")

def setupmove():
    replacements = {'THUMBNAILSFOLDER':THUMBNAILSFOLDER, 'oldthumbs':oldthumbs, 'newthumbs':newthumbs,
    'savevideodbfile':savevideodbfile, 'olddb':olddb, 'savetexturesdbfile':savetexturesdbfile,
    'newdb':newdb, 'DATABASEFOLDER':DATABASEFOLDER}

    with open(readinfile) as infile, open(writeoutfile, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)





setupmove()
	
printstar()
print "testbatchedit.py has just been started"
printstar()
xbmc.executebuiltin('Notification(testbatchedit.py, started)')