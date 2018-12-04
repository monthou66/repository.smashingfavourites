# -*- coding: utf-8 -*-
import xbmc
import os
import time
import shutil

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFOLDER = os.path.join(USERDATA, "smashing")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
updatefile = os.path.join(SMASHINGTEMP, "miscfiles", "update.txt")



# set defaults
source = 'not set'
target = 'not set'
newversion = 'not set'
oldversion = 'not set'
updateaddonid = 'not set'
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
        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFILE)
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
        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFOLDER)
    xbmc.sleep(300)

def copyfolder():
    global error, error2, errornotification
    print 'running copyfolder()'
    shutil.copytree(source, target)
    xbmc.sleep(300)
    if not os.path.isdir(target):
        error = 'Problem with copyfolder() function'
        error2 = ('Copyfolder failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
    
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
        DELETEFILE = updatefile
        removefile()
        
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
    xbmc.executebuiltin('Notification(%s, finished)'% thisaddon)
    
        
        
        
        
        
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
    
    
    exit()

startaddon()
readupdatefile()
checkupdate()

            
            
