# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import os
import shutil
import socket

# Define places - some might not be needed yet
USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
DEFAULTADDONS = os.path.join(xbmc.translatePath('special://xbmc/addons/'))
addondatacontents = os.listdir(ADDONDATA)
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
host = socket.gethostname()
SPECIFIC = os.path.join(USERDATA, "smashing", "smashingspecifics", host)
MISCFILES = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISCFILES, "addons")
SMASHINGFAKEADDONS = os.path.join(SMASHINGADDONS, "myfakeaddons")
SMASHINGREPOS = os.path.join(SMASHINGADDONS, "repos")
SMASHINGSTANDALONEADDONS = os.path.join(SMASHINGADDONS, "thirdpartyaddons")  # includes dependencies
SMASHINGSTANDALONESWITHDEPENDENCIES = os.path.join(SMASHINGADDONS, "thirdpartyaddonswithdependencies")
SMASHINGADDONDATA = os.path.join(MISCFILES, "addon_data")
errormessage = 'none'
message = 'none'
message1 = 'none'
message2 = 'none'
# markers:
enableaddonsmarker = os.path.join(xbmc.translatePath('special://masterprofile'), 'smashingtemp', 'markers', 'enableaddonsrunning.txt')

FAVOURITESFILE = os.path.join(USERDATA, "favourites.xml")
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
LOGFOLDER = xbmc.translatePath('special://logpath')
OLDLOGFILE = os.path.join(LOGFOLDER, "kodi.old.log")
skinpath = xbmc.translatePath('special://skin')

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"  

def error():
    printstar()
    print ('Error running %s'% thisaddon)
    if not errormessage == 'none':
        print 'Reported error is:'
        print errormessage
    printstar()        
    xbmc.executebuiltin('Notification(Problem with %s, Check the log for details)'% thisaddon)
    exit()

def postmessage():
    global message, message1, message2
    if not message == 'none':
        printstar()
        print ('%s message:'% thisaddon)
        print message
        if not message1 == 'none':
            print message1
            if not message2 == 'none':
                print message2
        printstar()        
    message = 'none'
    message1 = 'none'
    message2 = 'none'

def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
#    a = sys.argv[1]
    printstar()
    print ('%s has started'% thisaddon)
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
    getos()
	
# Get os
def getos():
    global PLATFORM, message, message1
    if xbmc.getCondVisibility('system.platform.android'):
        PLATFORM = 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        PLATFORM = 'linux'
        if xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
            PLATFORM = 'libreelec'
        else:
            errormessage = 'Platform identifies as linux but not as libreelec.'
            error()
            
    elif xbmc.getCondVisibility('system.platform.windows'):
        PLATFORM = 'windows'
    else:
        errormessage = 'Unable to identify the system platform.'
        error()
    # log results:
    message = ('Hostname is %s' % host)
    message1 = ('You\'re using %s' % PLATFORM)
    postmessage()
    
def libreelecstuff():
    exit()


def copyaddondata():
    global errormessage
    # datafolders = list of all folders to copy
    # folderpaths = list of full paths to copy
    datafolders = []
    folderpaths = []
    firstfolder = os.path.join(SPECIFIC, PLATFORM, "addon_data")
    secondfolder = os.path.join(SPECIFIC, "addon_data")
    thirdfolder = SMASHINGADDONDATA

    d = 1
    while d < 4:
        if d == 1:
            if os.path.isdir(firstfolder):
                folder = firstfolder
                list = os.listdir(firstfolder)
            else:
                d = 2
        if d == 2:
            if os.path.isdir(secondfolder):
                folder = secondfolder
                list = os.listdir(secondfolder)
            else:
                d = 3
        if d ==3:
            folder = thirdfolder
            list = os.listdir(thirdfolder)
        c = 0
        num = len(list)
        while c < num:
            sub = list[c]
            if sub not in datafolders:
                datafolders.append(sub)
                path = os.path.join(folder, sub)
                folderpaths.append(path)
            c = c + 1
        d = d + 1
        
    # Check for folders already in the userdata/addon_data folder:
    alreadythere = []
    notthereyet = []
    notthereyetpaths = []
    c = 0
    overwrite = 'dunno'
    # don't forget len(folderpaths) = len(datafolders)
    while c < len(folderpaths):
        check = datafolders[c]
#        print ('check is %s'% check)
        checkfolder = folderpaths[c]
        if check in addondatacontents:
#            print ('%s is in addondatacontents'% check)
            if overwrite == 'no':
                alreadythere.append(check)
            elif overwrite == 'yes':
                notthereyet.append(check)
                notthereyetpaths.append(checkfolder)
            elif overwrite == 'dunno':
                options = []
                a = ('Replace data for %s only'% check)
                options.append(a)
                a = ('Replace data for all addons')
                options.append(a)
                a = ('Do not replace data for %s'% check)
                options.append(a)
                a = ('Do not replace data for any addon')
                options.append(a)
                Message = ('%s folder already present'% check)
                CHOOSE = xbmcgui.Dialog().select(Message, options)
#                printstar()
#                print ('CHOOSE is %s'% CHOOSE)
                if CHOOSE == 0:
                    overwrite = 'dunno'
                    notthereyet.append(check)
                    notthereyetpaths.append(checkfolder)
                elif CHOOSE == 1:
                    overwrite = 'yes'
                    notthereyet.append(check)
                    notthereyetpaths.append(checkfolder)
                elif CHOOSE == 2:
                    overwrite = 'dunno'
                    alreadythere.append(check)
                elif CHOOSE == 3:
                    overwrite = 'no'
                    alreadythere.append(check)
                else:
                    xbmc.executebuiltin('Notification(Action, cancelled)')
                    exit()                    
        else:
#            print ('%s is not in addondatacontents'% check)
            notthereyet.append(check)
            notthereyetpaths.append(checkfolder)
#        print ('overwrite is %s'% overwrite)
#        print ('CHOOSE is %s'% CHOOSE)
        c = c + 1
        
# checky check - take this out later
#    print ('Don\'t copy: %s'% alreadythere)
#    print ('Do copy: %s'% notthereyet)
    print 'Folders to copy are:'
    c = 0
    while c < len(notthereyetpaths):
        print notthereyetpaths[c]
        c = c + 1       

# delete existing folders:
    if len(notthereyet) > 0:
        length = len(notthereyet)
        
        c = 0
        while c < length:
        
#            print ('c is %d'% c)
        
            sub = notthereyet[c]
            delete = os.path.join(ADDONDATA, sub)
            
#            print ('sub is %s'% sub)
#            print ('delete is %s'% delete)
            
            if os.path.exists(delete):
                shutil.rmtree(delete)
            c = c + 1

    xbmc.sleep(300)       
# copy new folders into addon_data:
    if len(notthereyetpaths) > 0:
        length = len(notthereyetpaths)
        c = 0
        while c < length:
            source = notthereyetpaths[c]
            sub = notthereyet[c]
            target = os.path.join(ADDONDATA, sub)
            
#            shutil.copytree(source, target)
            try:
                shutil.copytree(source, target)
            except:
                xbmc.sleep(300)
                try:
                    shutil.copytree(source, target)
                except:
                    errormessage = ('couldn\'t copy %s folder to addon_data'% source)
                    error()
            c = c + 1
       
# check if current skin settings have changed - if yes reload skin:
    skin = os.path.basename(os.path.normpath(skinpath))
#    print ('skin is %s'% skin)
#    print ('already there is %s'% alreadythere)
    if skin in notthereyet:
        xbmc.executebuiltin('ReloadSkin()')
        
        xbmc.sleep(3000)


def installaddons():
    global addonfolderpath, listaddons, myaddonstoinstall
    addonstoexclude = []
    addonstoinstall = []
    disabledaddonstoinstall = []
    myaddonstoinstall = []
    standaloneaddonstoinstall = []
    standaloneswithdependenciestoinstall = []
    repostoinstall = []
    addonsfromkodirepotoinstall = []
    addonsfromlibreelecrepotoinstall = []
    addonsfromthirdpartyrepostoinstall = []
    firstfile = os.path.join(SPECIFIC, PLATFORM, "addons.conf")
    secondfile = os.path.join(SPECIFIC, PLATFORM, "excludeaddons.conf")
    thirdfile = os.path.join(SPECIFIC, PLATFORM, "fakeaddons.conf")
    fourthfile = os.path.join(SPECIFIC, PLATFORM, "myaddons.conf")
    fifthfile = os.path.join(SPECIFIC, PLATFORM, "repos.conf")    
    sixthfile = os.path.join(SPECIFIC, "addons.conf")
    seventhfile = os.path.join(SPECIFIC, "excludeaddons.conf")
    eighthfile = os.path.join(SPECIFIC, "fakeaddons.conf")
    ninthfile = os.path.join(SPECIFIC, "myaddons.conf")
    tenthfile = os.path.join(SPECIFIC, "repos.conf")
    fileeleven = os.path.join(SMASHINGADDONS, "install lists", "addons.conf")
    filetwelve = os.path.join(SMASHINGADDONS, "install lists", "fakeaddons.conf")
    filethirteen = os.path.join(SMASHINGADDONS, "install lists", "myaddons.conf")
    filefourteen = os.path.join(SMASHINGADDONS, "install lists", "repos.conf")
    c = 1
#    printstar()
#    print 'check 278'
    while c < 15:
        if c == 1:
            addonfile = firstfile
        elif c == 2:
            addonfile = secondfile
        elif c == 3:
            addonfile = thirdfile
        elif c == 4:
            addonfile = fourthfile
        elif c == 5:
            addonfile = fifthfile
        elif c == 6:
            addonfile = sixthfile
        elif c == 7:
            addonfile = seventhfile
        elif c == 8:
            addonfile = eighthfile
        elif c == 9:
            addonfile = ninthfile
        elif c == 10:
            addonfile = tenthfile
        elif c == 11:
            addonfile = fileeleven
        elif c == 12:
            addonfile = filetwelve
        elif c == 13:
            addonfile = filethirteen
        elif c == 14:
            addonfile = filefourteen
        
#        print ('c is %s'% c)
#        print ('addonfile to check is %s'% addonfile)
        
        if os.path.isfile(addonfile):
        
#            print ('%s does exist'% addonfile)
        
            with open(addonfile) as f:
                lines = f.readlines()
                length = len(lines)
                d = 0
                while d < length:
                    line = lines[d]
#                    print ('line is %s'% line)
                    check = line.strip()
#                    print ('check is %s'% check)
#                    checkstart = check[0:8]
#                    print ('checkstart is %s'% checkstart)
#                    if checkstart == 'kodirepo':
                    if check[0:1] == '#':
                        d = d + 1
                    else:
                        if check[0:12] == 'fromkodirepo':
                            addon = check.replace(check[:12], '').strip()
#                            print ('addon is %s'% addon)
#                            addon = check.replace(check[:8], '')
#                            print ('addon is %s'% addon)
#                            addon = addon.strip()
#                            print ('addon is %s'% addon)
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        addonsfromkodirepotoinstall.append(addon)
                        elif check[0:14] == 'thirdpartyrepo':
                            addon = check.replace(check[:14], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        repostoinstall.append(addon)
                        elif check[0:8] == 'fromrepo':
                            addon = check.replace(check[:8], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        addonsfromthirdpartyrepostoinstall.append(addon)
                        elif check[0:17] == 'fromlibreelecrepo':
                            addon = check.replace(check[:17], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        addonsfromlibreelecrepotoinstall.append(addon)
                        elif check[0:12] == 'frommyaddons':
                            addon = check.replace(check[:12], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        myaddonstoinstall.append(addon)
                        elif check[0:12] == 'fromdisabled':
                            addon = check.replace(check[:12], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        disabledaddonstoinstall.append(addon)
                        elif check[0:10] == 'standalone':
                            addon = check.replace(check[:10], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        standaloneaddonstoinstall.append(addon)
                        elif check[0:26] == 'standalonewithdependencies':
                            addon = check.replace(check[:26], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":
                                        addonstoinstall.append(addon)
                                        standaloneswithdependenciestoinstall.append(addon)                                        
                        elif check[0:7] == 'exclude':
                            addon = check.replace(check[:7], '').strip()
                            if not addon in addonstoexclude:
                                if not addon in addonstoinstall:
                                    if not addon == "":                                
                                        addonstoexclude.append(addon)
                        d = d + 1
#        else:
#            print ('%s file does not exist'% addonfile)
        c = c + 1
    printstar()
    enable = 'no'
    if len(addonstoinstall) > 0:
        print ('addonstoinstall: %s'% addonstoinstall)
    if len(addonstoexclude) > 0:
        print ('addonstoexclude: %s'% addonstoexclude)
    else:
        print 'No addons have been excluded from the install'
    if len(disabledaddonstoinstall) > 0:
        enable = 'yes'
        print ('Disabled addons to install: %s'% disabledaddonstoinstall)
        listaddons = disabledaddonstoinstall
        addonfolderpath = SMASHINGFAKEADDONS
        copyandenable()
    if len(repostoinstall) > 0:
        enable = 'yes'
        print ('Third party repos to install: %s'% repostoinstall)
        listaddons = repostoinstall
        addonfolderpath = SMASHINGREPOS
        copyandenable()        
    if len(myaddonstoinstall) > 0:
        enable = 'yes'
        print ('My addons to install: %s'% myaddonstoinstall)
        installmyaddons()
    if len(standaloneaddonstoinstall) > 0:
        enable = 'yes'
        print ('Standalone third party addons to install: %s'% standaloneaddonstoinstall)
        listaddons = standaloneaddonstoinstall
        addonfolderpath = SMASHINGSTANDALONEADDONS
        copyandenable()
    if len(standaloneswithdependenciestoinstall) > 0:
        print ('standaloneswithdependenciestoinstall: %s'% standaloneswithdependenciestoinstall)        
    if len(addonsfromkodirepotoinstall) > 0:
        print ('addonsfromkodirepotoinstall: %s'% addonsfromkodirepotoinstall)
        listaddons = addonsfromkodirepotoinstall
        installfromrepo()
    if len(addonsfromlibreelecrepotoinstall) > 0:
        print ('Addons to install from the libreelec repo: %s'% addonsfromlibreelecrepotoinstall)
        listaddons = addonsfromlibreelecrepotoinstall
        installfromrepo()
    if len(addonsfromthirdpartyrepostoinstall) > 0:
        print ('Addons to install from third party repos: %s'% addonsfromthirdpartyrepostoinstall)
        listaddons = addonsfromthirdpartyrepostoinstall
        installfromrepo()
    printstar()
    # if any addons have been copied across they need to be enabled:
    if enable == 'yes':
        print 'check 450'
        if os.path.exists(enableaddonsmarker):
            os.remove(enableaddonsmarker)
        xbmc.executebuiltin('RunScript(special://masterprofile/smashing/smashingfavourites/scripts/utilityscripts/enableaddons.py)')
        c = 0
        while c < 100:
            print ('c is %s'% c)
            xbmc.sleep(300)
            if os.path.exists(enableaddonsmarker):
                c = c + 1
            else:
                c = 101
    print 'check 462'
    if os.path.exists(enableaddonsmarker):
        os.remove(enableaddonsmarker)
    print 'check 465'
    xbmc.sleep(300)
    print 'rowlocks'
    xbmc.executebuiltin('Notification(All, done)')        
    
def copyandenable():
    global errormessage
    printstar()
    print 'running copyandenable'
    length = len(listaddons)
    print ('length is %s'% length)
    c = 0
    while c < length:
        sub = listaddons[c]
        source = os.path.join(addonfolderpath, sub)
        target = os.path.join(ADDONS, sub)
        print ('source is %s'% source)
        print ('target is %s'% target)
        if os.path.exists(source):
            print ('%s exists - check'% source)
            if not os.path.exists(target):
                print ('trying to copy %s'% sub)
                try:
                    shutil.copytree(source, target)
                except:
                    xbmc.sleep(300)
                    try:
                        shutil.copytree(source, target)
                    except:
                        errormessage = ('Could not copy %s folder to %s'% (source, target))
                        error()
        else:
            print ('%s does not exist'% source)
        c = c + 1                  

def installmyaddons():
    alladdonfolders = []
    mysourcepaths = []
    mytargets = []
    alladdonfolders = os.listdir(SMASHINGADDONS)
    num = len(myaddonstoinstall)
    length = len(alladdonfolders)
    c = 0
    while c < length:
        folder = alladdonfolders[c]
        if folder[0:2] == 'my':
            folderpath = os.path.join(SMASHINGADDONS, folder)
            foldercontents = os.listdir(folderpath)
            d = 0
            while d < num:
                check = myaddonstoinstall[d]
                if check in foldercontents:
#                    printstar()
#                    print 'flippin eck'
                    addthis = os.path.join(folderpath, check)
                    mysourcepaths.append(addthis)
                    mytargets.append(check)
#                    print ('%s is the path I want'% addthis) 
                d = d + 1
        c = c + 1
    if len(mysourcepaths) > 0:
        length = len(mysourcepaths)
        c = 0
        while c < length:
            source = mysourcepaths[c]
            sub = mytargets[c]
            target = os.path.join(ADDONS, sub) 
            if os.path.exists(source):
                print ('%s exists - check'% source)
                if not os.path.exists(target):
                    print ('trying to copy %s'% sub)
                    try:
                        shutil.copytree(source, target)
                    except:
                        xbmc.sleep(300)
                        try:
                            shutil.copytree(source, target)
                        except:
                            errormessage = ('Could not copy %s folder to %s'% (source, target))
                            error()
            else:
                print ('%s does not exist'% source)
            c = c + 1 

def installfromrepo():
    global errormessage
    length = len(listaddons)
    c = 0
    while c < length:
        addon = listaddons[c]
        if  not xbmc.getCondVisibility('System.HasAddon(%s)' % addon):
            addonpath = os.path.join(ADDONS, addon)
            defaultaddonpath = os.path.join(DEFAULTADDONS, addon)
            if not os.path.exists(addonpath):
                print ('addon not found at addonpath: %s'% addonpath)
                if not os.path.exists(defaultaddonpath):
                    print ('addon not found at defaultaddonpath: %s'% defaultaddonpath)
                    xbmc.executebuiltin('InstallAddon(%s)'% addon)
                    xbmc.sleep(1000)
                    xbmc.executebuiltin('SendClick(11)')
                    addonpath = os.path.join(ADDONS, addon)
                    d = 0
                    while d < 100:
                        xbmc.sleep(2000)
                        if os.path.exists(addonpath):
                            xbmc.sleep(1000)
                            if xbmc.getCondVisibility('System.HasAddon(%s)' % addon):
                                d = 101
                        else:
                            d = d + 1
                    if  not xbmc.getCondVisibility('System.HasAddon(%s)' % addon):
                        errormessage = ('cannot install %s from repo'% addon)
                        error()
        c = c + 1
                



            
startaddon()

if PLATFORM == 'libreelec':
    libreelecstuff()

copyaddondata()

installaddons() 
   
exit()    
    
    



