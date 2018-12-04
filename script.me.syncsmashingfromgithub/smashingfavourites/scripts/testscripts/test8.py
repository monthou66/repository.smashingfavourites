# -*- coding: utf-8 -*-
import xbmc
import os
import shutil
import subprocess
from subprocess import Popen
# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")	
AUTOEXEC = os.path.join(USERDATA, "autoexec.py")
TEMPEXEC = os.path.join(SMASHINGFAVOURITES, "miscfiles", "slowstartupautoexec", "autoexec.py")


# Get os
def getos():
    global PLATFORM
    if xbmc.getCondVisibility('system.platform.android'):
        PLATFORM = 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        PLATFORM = 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        PLATFORM = 'windows'
    else:
        SYSPLAT = sys.platform
        printstar()
        print ('God only knows what platform this is!  sys.platform reurns %s' % SYSPLAT)
        printstar()
        exit()

def restartkodi():
# windows specific
    if PLATFORM == 'windows':
#        print 'platform is windows'
        # autoexec.py (make it automatically removeable)
        if not os.path.exists(AUTOEXEC) and os.path.isfile(TEMPEXEC):
            shutil.copy(TEMPEXEC, AUTOEXEC)	
        # check whether running portable install
        USERDATA = xbmc.translatePath('special://masterprofile')
        firsteightletters = USERDATA[:8]
        if firsteightletters == 'C:\Users':
            build = 'boring'
        else:
            build = 'portable'		
        # make sure batch has the correct shortcut			
        batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch")
        restartbat = os.path.join(batchfolder, "restart.bat")
        templatebat = os.path.join(batchfolder, "templaterestart.bat")
        kodiroot = xbmc.translatePath('special://xbmc')
        pathtokodiexe = os.path.join(kodiroot, "kodi.exe")
        if build == 'boring':
#            newline = 'START "" "E:\XBMC Stuff\kryptonmess\kodi.exe"'
            newline = ('START "" "%s"' % pathtokodiexe)
        elif build == 'portable':
#            newline = 'START "" "E:\XBMC Stuff\kryptonmess\kodi.exe" -p'
            newline = ('START "" "%s" -p' % pathtokodiexe)
        else:
            print 'bugger'
            exit()
        print ('newline = %s' % newline)
        # read current - maybe it's already there.
        if os.path.exists(restartbat) and os.path.isfile(restartbat):
            lines = file(restartbat, 'r').readlines()
            lastline = lines[-1].rstrip()
        else:
            lastline = 'not on your nelly'
        if lastline != newline:
            if os.path.exists(restartbat):
                os.remove(restartbat)
            shutil.copy(templatebat, restartbat)
            with open(restartbat, "a") as myfile:
                myfile.write(newline)
        else:
            print 'batch file correct already'
        # start batch
        batchfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "batch")
        batchfile = os.path.join(batchfolder, "restart.bat")
        assert os.path.isdir(batchfolder)
        os.chdir(batchfolder)
# Visible    subprocess.Popen('test.bat')
        subprocess.Popen('restart.bat',  shell=True)
        xbmc.sleep(1000)
        xbmc.executebuiltin('Quit')

# linux (libreelec) specific 
    elif PLATFORM == 'linux':
#        print 'platform is linux'	
        # start shell script
        shellfolder = os.path.join(SMASHINGFAVOURITES, "scripts", "shell")
        shellfile = os.path.join(shellfolder, "simplerestartkodi.sh")
        if os.path.isfile(shellfile):
            os.system('sh %s post' % shellfile)
 
# android fail
    elif PLATFORM == 'android':
        xbmc.executebuiltin('Notification(Sorry, This doesn\'t work on Android)')
        exit()

getos()
restartkodi()
# Drink beer        
