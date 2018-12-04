# -*- coding: utf-8 -*-
        
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

def copyfolder():
    global error, error2, errornotification, DELETEFOLDER, forcecopy
    print 'running copyfolder()'
    if not os.path.isdir(SOURCE):
        error = 'Problem with copyfolder() function'
        error2 = ('SOURCE folder (%s) does not exist'% SOURCE)
        errormessage()
    if os.path.isdir(TARGET):
        # check if TARGET is an empty folder.  If it isn't generate an error
        if os.listdir(TARGET) == []:
            try:
                os.rmdir(TARGET)
            except:
                error = 'Problem with copyfolder() function'
                error2 = ('Can\'t delete TARGET folder (%s)'% TARGET)
                errormessage()
        else:
            if forcecopy == 'true':
                DELETEFOLDER = TARGET
                removefolder()
            else:
                error = 'Problem with copyfolder() function'
                error2 = ('TARGET folder already exists(%s)'% TARGET)
                errormessage()
    shutil.copytree(SOURCE, TARGET)
    if not os.path.isdir(TARGET):
        error = 'Problem with copyfolder() function'
        error2 = ('Copyfolder failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
    forcecopy = 'false'
    
def copyfile():
    global error, error2, errornotification, DELETEFILE, forcecopy
    print 'running copyfile()'
    if not os.path.isfile(SOURCE):
        error = 'Problem with copyfile() function'
        error2 = ('SOURCE file (%s) does not exist'% SOURCE)
        errormessage()    
    if os.path.isfile(TARGET):
        if forcecopy == 'true':
            DELETEFILE = TARGET
            removefile()
        else:
            error = 'Problem with copyfile() function'
            error2 = ('TARGET file (%s) already exists'% TARGET)
            errormessage()
    try:
        shutil.copyfile(SOURCE, TARGET)
    except:
        error = 'Problem with copyfile() function'
        error2 = ('Copyfile failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
    forcecopy = 'false'
        
def movefolder():
    global error, error2, errornotification, DELETEFOLDER, forcemove
    print 'running movefolder()'
    if not os.path.isdir(SOURCE):
        error = 'Problem with movefolder() function'
        error2 = ('SOURCE folder (%s) does not exist'% SOURCE)
        errormessage()
    if os.path.isdir(TARGET):
        # check if TARGET is an empty folder.  If it isn't generate an error
        if os.listdir(TARGET) == []:
            try:
                os.rmdir(TARGET)
            except:
                error = 'Problem with movefolder() function'
                error2 = ('Can\'t delete TARGET folder (%s)'% TARGET)
                errormessage()
        else:
            if forcemove == 'true':
                DELETEFOLDER = TARGET
                removefolder()
            else:
                error = 'Problem with movefolder() function'
                error2 = ('TARGET folder already exists(%s)'% TARGET)
                errormessage()
    shutil.move(SOURCE, TARGET)                         # check this - is TARGET new folder name?
    if not os.path.isdir(TARGET):
        error = 'Problem with movefolder() function'
        error2 = ('Movefolder failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
    forcemove = 'false'

def movefile():
    global error, error2, errornotification, DELETEFILE, forcemove
    print 'running movefile()'       
    if not os.path.isfile(SOURCE):
        error = 'Problem with movefile() function'
        error2 = ('SOURCE file (%s) does not exist'% SOURCE)
        errormessage()
    if os.path.isfile(TARGET):
        if forcemove == 'true':
            DELETEFILE = TARGET
            removefile()
        else:
            error = 'Problem with movefile() function'
            error2 = ('TARGET file already exists(%s)'% TARGET)
            errormessage()
    shutil.move(SOURCE, TARGET)                         # check this - is TARGET new file name?
    if not os.path.isfile(TARGET):
        error = 'Problem with movefile() function'
        error2 = ('Movefile failed (%s to %s)'% (SOURCE, TARGET))
        errormessage()
    forcemove = 'false'        
      
  
  
