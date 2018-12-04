# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import os
import shutil
from subprocess import Popen

USERDATA = xbmc.translatePath('special://masterprofile')
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
# hackyhacks
restartheader = 'wibble'
db = 'wibble'
#thumbsdb = 'wobble'
# define db just for testing
db = 'local'
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def restartkodi():
    global thumbsdb
    global dbfolderdb
    restartwindow = xbmcgui.Dialog().ok(restartheader,"Click to re-start now and apply new settings")
    # Re-starting come what may - unless we're not!
    CHECKTHUMBS = os.path.join(USERDATA, "Thumbnails", "databaselocation.txt")
    CHECKDATABASE = os.path.join(USERDATA, "Database", "databaselocation.txt")
    if os.path.exists(CHECKTHUMBS) and os.path.isfile(CHECKTHUMBS):
        f = open(CHECKTHUMBS,'r')
        thumbsdb = f.read()
        thumbsdb = thumbsdb.strip()
        f.close()
    else:
        thumbsdb = 'wibblewobble'
        print 'problem - databaselocation.txt in Thumbnails folder is missing.  Making file.
        makedatabaselocation()
    if thumbsdb != db:
        print 'problem with databaselocation.txt in Thumbnails folder.  It does not match the old database type.'
        print '  Check it and try again.'
        restoreoldadvancedsettings()
		
    if os.path.exists(CHECKDATABASE) and os.path.isfile(CHECKDATABASE):
        f = open(CHECKDATABASE,'r')
        dbfolderdb = f.read()
        dbfolderdb = dbfolderdb.strip()
        f.close()
    else:
        dbfolderdb = 'wibblewobble'
        print 'problem - databaselocation.txt in Database folder is missing.  Making file.
        makedatabaselocation()
    if dbfolderdb != db:
        print 'problem with databaselocation.txt in Database folder.  It does not match the old database type.'
        print '  Check it and try again.'
        restoreoldadvancedsettings()
    # check whether databaselocation.txt matches the new database.  If it does match get on with it.
    # if not set batch file or shell script to move files (textures / videodb) and folder (Thumbnails) out and in.
	# Make sure all folders / files are ready to move
    if thumbsdb == CHOICE:
        justdoit()
    else:
        setupmove()
		
def makedatabaselocation():
    if thumbsdb = 'wibblewobble':
        checkfile = os.path.join(USERDATA, "Thumbnails", "databaselocation.txt")
    elif dbfolderdb = 'wibblewobble':
        checkfile = os.path.join(USERDATA, "Database", "databaselocation.txt")
    else:
        print 'problem with databaselocation.txt in Database folder.  It does not match the old database type.'
        print '  Check it and try again.'
        restoreoldadvancedsettings()
    if not os.path.exists(checkfile):
        # copy appropriate file into folder
        checkfolderfile = os.path.join(SMASHINGFAVOURITES, "databaselocationfiles", db, "databaselocation.txt")
        if os.path.exists(checkfolderfile) and os.path.isfile(checkfolderfile):
            shutil.copy(checkfolderfile, checkfile)
            print ('Copied databaselocation.txt to %s' % checkfile)
            restartkodi()
        else:
            print 'problem with databaselocation.txt in Database folder.  It does not match the old database type.'
            print '  Check it and try again.'
            restoreoldadvancedsettings()
    else:
        print 'problem with databaselocation.txt in Database folder.  It does not match the old database type.'
        print '  Check it and try again.'
        restoreoldadvancedsettings()			
			
			
def restoreoldadvancedsettings():
    # Get old settings (tst), get new settings (CHOICE)
    OLDADVSETTS = os.path.join(FOLDERSPATH, tst, "advancedsettings.xml")
    if tst == CHOICE:
        print 'advanced settings have not changed."
        exit()
    else:
        if os.path.exists(OLDADVSETTS) and os.path.isfile(OLDADVSETTS):
            os.remove(ADVANCEDSETTINGS)
            shutil.copy(, ADVANCEDSETTINGS)
            print 'advancedsettings.xml has been restored.'
            exit()
        else:
            print 'I just have no idea what's gone on there'
            exit()

def setupmove():
    # for windows / linux: set up batch / shell scrip to move files / folders
    oldthumbs = os.path.join(USERDATA, "Backup.%s", "Thumbnails" % db)
    newthumbs = os.path.join(USERDATA, "Backup.%s", "Thumbnails" % CHOICE)
    olddb = os.path.join(USERDATA, "Backup.%s", "Database" % db)
    newdb = os.path.join(USERDATA, "Backup.%s", "Database" % CHOICE)
    # DATABASEFOLDER = os.path.join(USERDATA, "Database")
    # THUMBNAILSFOLDER = os.path.join(USERDATA, "Thumbnails")
    if PLATFORM == 'windows':
        batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch")
        writeoutfile = os.path.join(batchfolder, "restartkodiadvsetts.bat")
        readinfile = os.path.join(batchfolder, "templaterestartkodiadvsetts.bat")		
    elif PLATFORM == 'linux':
        shellfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "shell")
        writeoutfile = os.path.join(shellfolder, "restartkodiadvsetts.sh")
        readinfile = os.path.join(shellfolder, "templaterestartkodiadvsetts.sh")
		
    replacements = {'THUMBNAILSFOLDER':THUMBNAILSFOLDER, 'oldthumbs':oldthumbs, 'newthumbs':newthumbs,
    'savevideodbfile':savevideodbfile, 'olddb':olddb, 'savetexturesdbfile':savetexturesdbfile,
    'newdb':newdb, 'DATABASEFOLDER':DATABASEFOLDER}

    with open(readinfile) as infile, open(writeoutfile, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)	
    justdoit()			
		
def justdoit():
    # set up checkadvancedsettings.xml (autoexec.py), run batch or shell script and restart
    AUTOEXEC = os.path.join(USERDATA, "autoexec.py")
    TEMPEXEC = os.path.join(SMASHINGFAVOURITES, "miscfiles", "checkadvancedsettingsautoexec", "autoexec.py")
    if os.path.exists(AUTOEXEC) and os.path.isfile(AUTOEXEC):
        # write 2 lines to the end of the existing autoexec.py file.  Assume it already contains 'import XBMC'
        with open(AUTOEXEC, "a") as myfile:
            myfile.write("xbmc.executebuiltin('XBMC.RunScript(special://masterprofile/smashing/smashingfavourites/scripts/advancedsettings/checkadvancedsettings.py)')")
            myfile.write("#permanent")	
    else:
        shutil.copy(TEMPEXEC, AUTOEXEC)
    if PLATFORM == 'windows':
    # start batch
    batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch")
    batchfile = os.path.join(batchfolder, "restartkodiadvsetts.bat")
    # check if batch file is in place.  If not that means a simple restart, so move that file in.
    if not os.path.exists(batchfile):
        simplerestartbatchfile = os.path.join(batchfolder, "simplerestartkodiadvsetts.bat")
        shutil.copy(simplerestartbatchfile, batchfile)
    p = Popen(batchfile, cwd=rbatchfolder)			###Check!
    stdout, stderr = p.communicate()
    # close kodi
    xbmc.executebuiltin('Quit')	
		
    elif PLATFORM == 'linux':
    # start shell
    shellfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "shell")	
    shellfile = os.path.join(shellfolder, "restartkodiadvsetts.sh")
        # check if shell file is in place.  If not that means a simple restart, so move that file in.
    if not os.path.exists(shellfile):
        simplerestartshellfile = os.path.join(shellfolder, "simplerestartkodiadvsetts.sh")
        shutil.copy(simplerestartshellfile, shellfile)	
    # restart
    os.system('sh %s post' % shellfile)				###Check!
	
    elif PLATFORM == 'android':
    # Gawd only knows
	
	
	
    else:
    # Just give up
	
		
#testrestart
restart()		
printstar()
print "test5.py has just been started"
print ('thumbsdb = %s' % thumbsdb)
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')
exit()	
	
def toggledebug():
    # read debug line in log, change as required
    # restart kodi
    global restartheader
    if debugsetting == 'enable':
        delete_start = ["loglevel>0<"]
        replacestart = "loglevel>1<"
        expected = '<loglevel>0</loglevel>'
        unexpected = '<loglevel>1</loglevel>'
    elif debugsetting == 'disable':
        delete_start = ["loglevel>1<"]
        replacestart = "loglevel>0<"
        expected = '<loglevel>1</loglevel>'
        unexpected = '<loglevel>0</loglevel>'		
    else:
        print 'problem detected - no valid debugsetting found.'
        exit()	    
    if os.path.exists(ADVANCEDSETTINGS) and os.path.isfile(ADVANCEDSETTINGS):
        lines = file(ADVANCEDSETTINGS, 'r').readlines()
        debugcurrent = lines[-11].strip()
        if debugcurrent == expected:
            # edit file
            infile = ADVANCEDSETTINGS
            outfile = os.path.join(USERDATA, "advancedsettingstemp.xml")
#            delete_start = ["loglevel>0<"]
            delete_end = ["/loglevel"]
            fin = open(infile)
            fout = open(outfile, "w+")
            for line in fin:
                for word in delete_start:
                    line = line.replace(word, replacestart)
                for word in delete_end:
                    line = line.replace(word, "/loglevel")	
                fout.write(line)
            fin.close()
            fout.close()
            os.remove(infile)
            os.rename(outfile, infile)
            restartheader = ('Debug logging has been %sd in advanced settings' % debugsetting)
            restartkodi()
        elif debugcurrent == unexpected:
            restartheader = ('Debug logging was already %sd in advanced settings' % debugsetting)
            restartkodi()			
        else:
            print 'No log settings found.'
            print ('debugcurrent = %s' % debugcurrent)
    else:
        print 'No advanced settings found.'








debugsetting = 'enable'
toggledebug()	
printstar()
print "test5.py has just been started"
print 'done it by George'
printstar()
xbmc.executebuiltin('Notification(test5.py, started)')