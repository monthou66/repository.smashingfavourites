# -*- coding: utf-8 -*-
import xbmc
import os
import time
import shutil
import xbmcvfs

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFOLDER = os.path.join(USERDATA, "smashing")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
updatefile = os.path.join(SMASHINGTEMP, "miscfiles", "update.txt")



# set defaults
source = 'not set'
target = 'not set'
newversion = 'not set'
oldversion = 'not set'
updateaddonid = 'Addon'
fileisold = 'not set'
force = 'false'
quiet = 'false'
invalidtarget = 'false'
invalidsource = 'false'
age = 1000
# default messages
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
error3 = 'none'
errornotification = 'none'

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def startaddon():
    global thisaddon, source, target, updateaddonid, error, error2
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    num = len(sys.argv)
    if num == 1:
        readupdatefile()
    else:
        c = 1
        while c < num:
            check = sys.argv[c]
            if check[:9] == 'source = ':
                source = check[9:]
                source = source.strip()
            elif check[:7] == 'dest = ':
                target = check[7:]
                target = target.strip()
            elif check[:16] == 'updateaddonid = ':
                updateaddonid = check[16:]
                updateaddonid = updateaddonid.strip()
            elif check == 'choose':
                chooseupdate()
            else:
                error = 'problem in startaddon()'
                error2 = ('argument not recognised (%s)'% check)
                errormessage()
            c = c + 1
            checkupdate
    
# errors
def errormessage():
    global error, error2, errornotification
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    if error in globals():
        if not error == 'none':
            print error
    if error2 in globals():
        if not error2 == 'none':
            print error2
    if error3 in globals():
        if not error3 == 'none':
            print error3
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    if errornotification in globals():
        if not errornotification == 'none':
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(errornotification)')
    printstar()
    cleanup()

def removefile():
    global error, error2, errornotification
    print 'running removefile()'
    print ('DELETEFILE is %s'% DELETEFILE)
    # delete file
    # DELETEFILE = the full path of the file to be removed
    if os.path.exists(DELETEFILE):
        count = 0
        while count < 50:
            try:
                os.remove(DELETEFILE)
            except:
                pass
            print ('checking for %s'% DELETEFILE)
            if not os.path.exists(DELETEFILE):
                print 'DELETEFILE has been removed'
                count = count + 50
            else:
                xbmc.sleep(300)
                print 'Oh no it hasn\'t'
                count = count + 1
    if os.path.exists(DELETEFILE):
        error = ('Problem with removefile() function in %s.'% thisaddon)
        error2 = ('Could not delete the file at %s'% DELETEFILE)
        printstar()
        errornotification = ('Something went wrong, Could not delete %s'% DELETEFILE)
        errormessage()
    else:
        printstar()
        print ('%s has deleted %s'% (thisaddon, DELETEFILE))
        printstar()
#        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFILE)
    xbmc.sleep(300) 
    
 # remove a folder recursively
def removefolder():
    global error, error2, errornotification
    print 'running removefolder()'
    print ('DELETEFOLDER is %s'% DELETEFOLDER)
    # delete folder
    # DELETEFOLDER = the full path of the folder to be removed
    if os.path.exists(DELETEFOLDER):
        count = 0
        while count < 50:
            try:
                shutil.rmtree(DELETEFOLDER)
            except:
                pass
            print ('checking for %s'% DELETEFOLDER)
            if not os.path.exists(DELETEFOLDER):
                print 'DELETEFOLDER has been removed'
                count = count + 50
            else:
                xbmc.sleep(300)
                print 'Oh no it hasn\'t'
                count = count + 1
    if os.path.exists(DELETEFOLDER):
        error = ('Problem with removefolder() function in %s.'% thisaddon)
        error2 = ('Could not delete the folder at %s'% DELETEFOLDER)
        printstar()
        errornotification = ('Something went wrong, Could not delete %s'% DELETEFOLDER)
        errormessage()
    else:
        printstar()
        print ('%s has deleted %s'% (thisaddon, DELETEFOLDER))
        printstar()
#        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFOLDER)
    xbmc.sleep(300)

def oldcopyfolder():
    global error, error2, errornotification
    print 'running copyfolder()'
    shutil.copytree(source, target)
    xbmc.sleep(300)
    if not os.path.isdir(target):
        error = 'Problem with copyfolder() function'
        error2 = ('Copyfolder failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()

def copyfolder():
    global error, error2, errornotification, next
    print 'running copyfolder()'
    os.mkdir(target)
    dirs = []
    files = []
    dirs, files = xbmcvfs.listdir(source)
    print ('source is: %s'% source)
    num = len(dirs)
    print ('num = %d'% num)
    if num == 0:
        print 'No subfolders - end of the line'
        # pass
    else:
        c = 0
        print 'Subfolders in source are:'
        while c < num:
            next = dirs[c]
            print next
            targetdir = os.path.join(target, next)
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel2()
            c = c + 1
    num = len(files)
    print ('num = %d'% num)
    if num == 0:
        print 'No files in source'
        # pass
    else:
        c = 0
        print 'Files in source are:'
        while c < num:
            next = files[c]
            print next
            sourcefile = os.path.join(source, next)
            targetfile = os.path.join(target, next)
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1
            
def copylevel2():
    global next, next2, sourcelevel2, targetlevel2
    print 'running copylevel2()'
    level2files = []
    level2dirs = []
    sourcelevel2 = os.path.join(source, next)
    targetlevel2 = os.path.join(target, next)
    level2dirs, level2files = xbmcvfs.listdir(sourcelevel2)
    print ('sourcelevel2 is: %s'% sourcelevel2)
    numlevel2 = len(level2dirs)
    print ('numlevel2 = %d'% numlevel2)
    if numlevel2 == 0:
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel2 are:'
        while c < numlevel2:
            next2 = level2dirs[c]
            print next2
            targetdir = os.path.join(targetlevel2, next2)
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel3()
            c = c + 1
    numlevel2 = len(level2files)
    print ('numlevel2 = %d'% numlevel2)
    if numlevel2 == 0:
        print 'No files in sourcelevel2'
    else:
        c = 0
        print 'Files in sourcelevel2 are:'
        while c < numlevel2:
            next2 = level2files[c]
            print next2
            sourcefile = os.path.join(sourcelevel2, next2)
            targetfile = os.path.join(targetlevel2, next2)
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1

            
def copylevel3():
    global next2, next3, sourcelevel3, targetlevel3
    print 'running copylevel3()'
    level3files = []
    level3dirs = []
    sourcelevel3 = os.path.join(sourcelevel2, next2)
    targetlevel3 = os.path.join(targetlevel2, next2)
    level3dirs, level3files = xbmcvfs.listdir(sourcelevel3)
    print ('sourcelevel3 is: %s'% sourcelevel3)
    numlevel3 = len(level3dirs)
    print ('numlevel3 = %d'% numlevel3)
    if numlevel3 == 0:
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel3 are:'
        while c < numlevel3:
            next3 = level3dirs[c]
            print ('next3 is %s'% next3)
            targetdir = os.path.join(targetlevel3, next3)
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel4()
            c = c + 1
    numlevel3 = len(level3files)
    print ('numlevel3 = %d'% numlevel3)
    if numlevel3 == 0:
        print 'No files in sourcelevel3'
    else:
        c = 0
        print 'Files in sourcelevel3 are:'
        while c < numlevel3:
            next3 = level3files[c]
            print ('next3 is %s'% next3)
            sourcefile = os.path.join(sourcelevel3, next3)
            print ('copylevel3sourcefile is %s'% sourcefile)
            targetfile = os.path.join(targetlevel3, next3)
            print ('copylevel3targetfile is %s'% targetfile)
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1            

def copylevel4():
    global next3, next4, sourcelevel4, targetlevel4
    print 'running copylevel4()'
    level4files = []
    level4dirs = []
    sourcelevel4 = os.path.join(sourcelevel3, next3)
    targetlevel4 = os.path.join(targetlevel3, next3)
    level4dirs, level4files = xbmcvfs.listdir(sourcelevel4)
    print ('sourcelevel4 is: %s'% sourcelevel4)
    numlevel4 = len(level4dirs)
    if numlevel4 == 0:
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel4 are:'										# change 1 number
        while c < numlevel4:														# change 1 number
            next4 = level4dirs[c]													# change 2 numbers
            print ('next4 is %s'% next4)											# change 2 numbers
            targetdir = os.path.join(targetlevel4, next4)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel5()															# change 1 number
            c = c + 1
    numlevel4 = len(level4files)													# change 2 numbers
    print ('numlevel4 = %d'% numlevel4)												# change 2 numbers
    if numlevel4 == 0:
        print 'No files in sourcelevel4'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel4 are:'											# change 1 number
        while c < numlevel4:														# change 1 number
            next4 = level4files[c]													# change 2 numbers
            print ('next4 is %s'% next4)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel4, next4)							# change 2 numbers
            print ('copylevel4sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel4, next4)							# change 2 numbers
            print ('copylevel4targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel5():																	# change name
    global next4, next5, sourcelevel5, targetlevel5									# change 4 numbers
    print 'running copylevel5()'													# change 1 number
    level5files = []																# change 1 number
    level5dirs = []																	# change 1 number
    sourcelevel5 = os.path.join(sourcelevel4, next4)								# change 3 numbers
    targetlevel5 = os.path.join(targetlevel4, next4)								# change 3 numbers
    level5dirs, level5files = xbmcvfs.listdir(sourcelevel5)							# change 3 numbers
#    print ('sourcelevel5 is: %s'% sourcelevel5)										# change 2 numbers
    numlevel5 = len(level5dirs)														# change 2 numbers
#    print ('numlevel5 = %d'% numlevel5)												# change 2 numbers
    if numlevel5 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
#        print 'Subfolders in sourcelevel5 are:'										# change 1 number
        while c < numlevel5:														# change 1 number
            next5 = level5dirs[c]													# change 2 numbers
#            print ('next5 is %s'% next5)											# change 2 numbers
            targetdir = os.path.join(targetlevel5, next5)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel6()															# change 1 number
            c = c + 1
    numlevel5 = len(level5files)													# change 2 numbers
#    print ('numlevel5 = %d'% numlevel5)												# change 2 numbers
    if numlevel5 == 0:
        print 'No files in sourcelevel5'											# change 1 number
    else:
        c = 0
#        print 'Files in sourcelevel5 are:'											# change 1 number
        while c < numlevel5:														# change 1 number
            next5 = level5files[c]													# change 2 numbers
#            print ('next5 is %s'% next5)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel5, next5)							# change 2 numbers
#            print ('copylevel5sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel5, next5)							# change 2 numbers
#            print ('copylevel5targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1 

def copylevel6():																	# change name
    global next5, next6, sourcelevel6, targetlevel6									# change 4 numbers
    print 'running copylevel6()'													# change 1 number
    level6files = []																# change 1 number
    level6dirs = []																	# change 1 number
    sourcelevel6 = os.path.join(sourcelevel5, next5)								# change 3 numbers
    targetlevel6 = os.path.join(targetlevel5, next5)								# change 3 numbers
    level6dirs, level6files = xbmcvfs.listdir(sourcelevel6)							# change 3 numbers
#    print ('sourcelevel6 is: %s'% sourcelevel6)										# change 2 numbers
    numlevel6 = len(level6dirs)														# change 2 numbers
#    print ('numlevel6 = %d'% numlevel6)												# change 2 numbers
    if numlevel6 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
#        print 'Subfolders in sourcelevel6 are:'										# change 1 number
        while c < numlevel6:														# change 1 number
            next6 = level6dirs[c]													# change 2 numbers
#            print ('next6 is %s'% next6)											# change 2 numbers
            targetdir = os.path.join(targetlevel6, next6)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel7()															# change 1 number
            c = c + 1
    numlevel6 = len(level6files)													# change 2 numbers
#    print ('numlevel6 = %d'% numlevel6)												# change 2 numbers
    if numlevel6 == 0:
        print 'No files in sourcelevel6'											# change 1 number
    else:
        c = 0
#        print 'Files in sourcelevel6 are:'											# change 1 number
        while c < numlevel6:														# change 1 number
            next6 = level6files[c]													# change 2 numbers
#            print ('next6 is %s'% next6)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel6, next6)							# change 2 numbers
#            print ('copylevel6sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel6, next6)							# change 2 numbers
#            print ('copylevel6targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel7():																	# change name
    global next6, next7, sourcelevel7, targetlevel7									# change 4 numbers
    print 'running copylevel7()'													# change 1 number
    level7files = []																# change 1 number
    level7dirs = []																	# change 1 number
    sourcelevel7 = os.path.join(sourcelevel6, next6)								# change 3 numbers
    targetlevel7 = os.path.join(targetlevel6, next6)								# change 3 numbers
    level7dirs, level7files = xbmcvfs.listdir(sourcelevel7)							# change 3 numbers
#    print ('sourcelevel7 is: %s'% sourcelevel7)										# change 2 numbers
    numlevel7 = len(level7dirs)														# change 2 numbers
#    print ('numlevel7 = %d'% numlevel7)												# change 2 numbers
    if numlevel7 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
#        print 'Subfolders in sourcelevel7 are:'										# change 1 number
        while c < numlevel7:														# change 1 number
            next7 = level7dirs[c]													# change 2 numbers
#            print ('next7 is %s'% next7)											# change 2 numbers
            targetdir = os.path.join(targetlevel7, next7)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel8()															# change 1 number
            c = c + 1
    numlevel7 = len(level7files)													# change 2 numbers
#    print ('numlevel7 = %d'% numlevel7)												# change 2 numbers
    if numlevel7 == 0:
        print 'No files in sourcelevel7'											# change 1 number
    else:
        c = 0
#        print 'Files in sourcelevel7 are:'											# change 1 number
        while c < numlevel7:														# change 1 number
            next7 = level7files[c]													# change 2 numbers
#            print ('next7 is %s'% next7)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel7, next7)							# change 2 numbers
#            print ('copylevel7sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel7, next7)							# change 2 numbers
#            print ('copylevel7targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel8():																	# change name
    global next7, next8, sourcelevel8, targetlevel8									# change 4 numbers
    print 'running copylevel8()'													# change 1 number
    level8files = []																# change 1 number
    level8dirs = []																	# change 1 number
    sourcelevel8 = os.path.join(sourcelevel7, next7)								# change 3 numbers
    targetlevel8 = os.path.join(targetlevel7, next7)								# change 3 numbers
    level8dirs, level8files = xbmcvfs.listdir(sourcelevel8)							# change 3 numbers
#    print ('sourcelevel8 is: %s'% sourcelevel8)										# change 2 numbers
    numlevel8 = len(level8dirs)														# change 2 numbers
#    print ('numlevel8 = %d'% numlevel8)												# change 2 numbers
    if numlevel8 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
#        print 'Subfolders in sourcelevel8 are:'										# change 1 number
        while c < numlevel8:														# change 1 number
            next8 = level8dirs[c]													# change 2 numbers
#            print ('next8 is %s'% next8)											# change 2 numbers
            targetdir = os.path.join(targetlevel8, next8)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel9()															# change 1 number
            c = c + 1
    numlevel8 = len(level8files)													# change 2 numbers
#    print ('numlevel8 = %d'% numlevel8)												# change 2 numbers
    if numlevel8 == 0:
        print 'No files in sourcelevel8'											# change 1 number
    else:
        c = 0
#        print 'Files in sourcelevel8 are:'											# change 1 number
        while c < numlevel8:														# change 1 number
            next8 = level8files[c]													# change 2 numbers
#            print ('next8 is %s'% next8)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel8, next8)							# change 2 numbers
#            print ('copylevel8sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel8, next8)							# change 2 numbers
#            print ('copylevel8targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel9():																	# change name
    global next8, next9, sourcelevel9, targetlevel9									# change 4 numbers
    print 'running copylevel9()'													# change 1 number
    level9files = []																# change 1 number
    level9dirs = []																	# change 1 number
    sourcelevel9 = os.path.join(sourcelevel8, next8)								# change 3 numbers
    targetlevel9 = os.path.join(targetlevel8, next8)								# change 3 numbers
    level9dirs, level9files = xbmcvfs.listdir(sourcelevel9)							# change 3 numbers
#    print ('sourcelevel9 is: %s'% sourcelevel9)										# change 2 numbers
    numlevel9 = len(level9dirs)														# change 2 numbers
#    print ('numlevel9 = %d'% numlevel9)												# change 2 numbers
    if numlevel9 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
#        print 'Subfolders in sourcelevel9 are:'										# change 1 number
        while c < numlevel9:														# change 1 number
            next9 = level9dirs[c]													# change 2 numbers
#            print ('next9 is %s'% next9)											# change 2 numbers
            targetdir = os.path.join(targetlevel9, next9)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel10()															# change 1 number
            c = c + 1
    numlevel9 = len(level9files)													# change 2 numbers
#    print ('numlevel9 = %d'% numlevel9)												# change 2 numbers
    if numlevel9 == 0:
        print 'No files in sourcelevel9'											# change 1 number
    else:
        c = 0
#        print 'Files in sourcelevel9 are:'											# change 1 number
        while c < numlevel9:														# change 1 number
            next9 = level9files[c]													# change 2 numbers
#            print ('next9 is %s'% next9)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel9, next9)							# change 2 numbers
#            print ('copylevel9sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel9, next9)							# change 2 numbers
#            print ('copylevel9targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel10():																	# change name
    global next9, next10, sourcelevel10, targetlevel10									# change 4 numbers
    print 'running copylevel10()'													# change 1 number
    level10files = []																# change 1 number
    level10dirs = []																	# change 1 number
    sourcelevel10 = os.path.join(sourcelevel9, next9)								# change 3 numbers
    targetlevel10 = os.path.join(targetlevel9, next9)								# change 3 numbers
    level10dirs, level10files = xbmcvfs.listdir(sourcelevel10)							# change 3 numbers
#    print ('sourcelevel10 is: %s'% sourcelevel10)										# change 2 numbers
    numlevel10 = len(level10dirs)														# change 2 numbers
#    print ('numlevel10 = %d'% numlevel10)												# change 2 numbers
    if numlevel10 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
#        print 'Subfolders in sourcelevel10 are:'										# change 1 number
        while c < numlevel10:														# change 1 number
            next10 = level10dirs[c]													# change 2 numbers
#            print ('next10 is %s'% next10)											# change 2 numbers
            targetdir = os.path.join(targetlevel10, next10)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel11()															# change 1 number
            c = c + 1
    numlevel10 = len(level10files)													# change 2 numbers
#    print ('numlevel10 = %d'% numlevel10)												# change 2 numbers
    if numlevel10 == 0:
        print 'No files in sourcelevel10'											# change 1 number
    else:
        c = 0
#        print 'Files in sourcelevel10 are:'											# change 1 number
        while c < numlevel10:														# change 1 number
            next10 = level10files[c]													# change 2 numbers
#            print ('next10 is %s'% next10)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel10, next10)							# change 2 numbers
#            print ('copylevel10sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel10, next10)							# change 2 numbers
#            print ('copylevel10targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel11():                                                                   # change 1 number
    global problem, listproblemfolders, next10, sourcelevel10						                        # change 2 numbers
    sourcefoldernotprocessed = os.path.join(sourcelevel10, next10)	                # change 2 numbers
    listproblemfolders.append(sourcefoldernotprocessed)
    print 'running copylevel11'                                                      # change 1 number
    print 'That means not everything has been copied!'
    problem = 'true'
            
def readupdatefile():
    global source, target, force, quiet, oldfile, DELETEFILE
    print 'running readupdatefile()'
    # read settings
    if os.path.isfile(updatefile):
        f = open(updatefile, "r")
        lines = f.readlines()
        f.close()
        num = len(lines)
        if num > 0:
            c = 0
            while c < num:
                check = lines[c]
                if check[:9] == 'source = ':
                    source = check[9:]
                    source = source.strip()
                elif check[:7] == 'dest = ':
                    target = check[7:]
                    target = target.strip()
                elif check[:13] == 'newversion = ':
                    newversion = check[13:]
                    newversion = newversion.strip()
                elif check[:13] == 'oldversion = ':
                    oldversion = check[13:]
                    oldversion = oldversion.strip()
                elif check[:16] == 'updateaddonid = ':
                    updateaddonid = check[16:]
                    updateaddonid = updateaddonid.strip()
                elif check[:5] == 'force':
                    force = 'true'
                elif check[:5] == 'quiet':
                    force = 'quiet'
                elif check[:1] == "":
                    pass
                elif check[:1] == '#':
                    pass
                c = c + 1
        # get time since updatefile was modified:
        st=os.stat(updatefile)    
        mtime=st.st_mtime
        now = time.time()
        age = now - mtime
        msg = 'file is %d seconds old'% age     
        # print settings
        print ('source is %s'% source)
        print ('target is %s'% target)
        print ('newversion is %s'% newversion)
        print ('oldversion is %s'% oldversion)
        print ('updateaddonid is %s'% updateaddonid)
        print ('force = %s'% force)
        print ('quiet = %s'% quiet)
        if not age == 1000:
            if age < 2:
                xbmc.sleep(2000)
                now = time.time()
                age = now - mtime
                msg = 'file is %d seconds old'% age
            print msg
            xbmc.executebuiltin('Notification(File checked:, %s)'% msg)
        if age > 10:
            oldfile = 'true'    
#        DELETEFILE = updatefile
#        removefile()
        
def checkupdate():
    global source, target, force, quiet, age, invalidtarget, invalidsource, DELETEFOLDER
    print 'running checkupdate'
    if target == 'not set':
        chooseaddon()
    if source == 'not set':
        choosesource()
    if not os.path.isdir(target):
        invalidtarget = 'true'
        chooseaddon()
    if not os.path.isdir(source):
        invalidsource = 'true'
        choosesource()
    if age > 10:
        checkoldupdatefile()
    DELETEFOLDER = target
    removefolder()
    copyfolder()
    cleanup()
    
        
        
        
        
        
def chooseaddon():
    global target, invalidtarget
    print 'running chooseaddon()'
    
    
def choosesource():
    global target, source, invalidsource
    print 'running choosesource()'
    
def checkoldupdatefile():
    global age
    print 'running checkoldupdatefile()'
    
def chooseupdate():
    global source, target, DELETEFOLDER
    print 'running chooseupdate()'
    
def cleanup():
    print 'running cleanup()'
#    xbmc.executebuiltin('Notification(%s, finished)'% thisaddon)
    xbmc.executebuiltin('Notification(%s, has been updated)'% updateaddonid)    
    exit()

startaddon()
readupdatefile()
checkupdate()

            
            
