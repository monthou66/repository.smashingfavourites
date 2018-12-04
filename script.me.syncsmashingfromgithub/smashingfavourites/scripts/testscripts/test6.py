# -*- coding: utf-8 -*-
# test edit batch
import xbmc
import os

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

USERDATA = xbmc.translatePath('special://masterprofile')
TEST = os.path.join(USERDATA, "test")
# need to define:
THUMBNAILSFOLDER = os.path.join(TEST, "Thumbnails")
oldthumbs = os.path.join(TEST, "OldThumbnails")
newthumbs = os.path.join(TEST, "OldThumbnails")
savevideodbfile = os.path.join(TEST, "savevideodbfile")
savetexturesdbfile = os.path.join(TEST, "savetexturesdbfile")
olddb = os.path.join(TEST, "olddb")
newdb = os.path.join(TEST, "newdb")
DATABASEFOLDER = os.path.join(TEST, "Database")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch")
writeoutfile = os.path.join(batchfolder, "restartkodiadvsetts.bat")
readinfile = os.path.join(batchfolder, "templaterestartkodiadvsetts.bat")

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