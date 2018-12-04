# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os
import shutil
import socket


# sources
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
# path to advancedsettings options folders:	
ADVANCEDSETTINGSFOLDER = os.path.join(SMASHINGFAVOURITES, "advancedsettings")
ADVSETTSTEMPLATES = os.path.join(ADVANCEDSETTINGSFOLDER, "templates")
IPADDRESSES = os.path.join(ADVSETTSTEMPLATES, "ipaddresses.xml")
TEMPLATE = os.path.join(ADVSETTSTEMPLATES, "templateadvancedsettings.xml")
DRIVESOURCES = os.path.join(ADVSETTSTEMPLATES, "drivesources.xml")
DEFAULTS = os.path.join(ADVSETTSTEMPLATES, "defaultvalues.xml")
PATHSUBS = os.path.join(ADVSETTSTEMPLATES, "pathsubs.xml")
# path to working advancedsettings.xml
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")


# defaults
force = 'false'
editcurrent = 'false'
driveshost = 'false'
driveshostip = 'false'
driveschecked = 'false'
mysql = 'false'
mysqlhostname = 'false'
mysqlip = 'false'
mysqlport = 'false'
mysqluser = 'false'
mysqlpass = 'false'
mysqlname = 'false'
locallibrary = 'false'
host = 'false'
platform = 'false'
extranames = []
extradetails = []
extraoption1 = 'none'
extraoption2 = 'none'
extraoption3 = 'none'
extraoption4 = 'none'
extraoption5 = 'none'
currentadvancedsettings = 'false'
currentdriveshost = 'false'
currentdriveshostip = 'false'
currentdriveschecked = 'false'
currentmysql = 'false'
currentmysqlhostname = 'false'
currentmysqlip = 'false'
currentlocallibrary = 'false'
currenthost = 'false'
currentplatform = 'false'
currentextranames = []
currentextradetails = []
currentextraoption1 = 'none'
currentextraoption2 = 'none'
currentextraoption3 = 'none'
currentextraoption4 = 'none'
currentextraoption5 = 'none'
currentdebugcurrent = 'false'
logmessage = 'none'
logmessage2 = 'none'
logmessage3 = 'none'
logmessage4 = 'none'
logmessage5 = 'none'
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
error3 = 'none'
error4 = 'none'
errornotification = 'none'
errordialogheader = 'none'
message = 'none'       # set default to 'none'; only print if changed

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"  

def printlog():
    global logmessage, logmessage2, logmessage3, logmessage4, logmessage5
    print 'running printlog()'
    getdateandtime()
    starter = ('\n%s %s'%(dateandtime, thisaddon))
    starter = (starter+"                                        ")[:55] # this adds 40 spaces to starter but cuts the max length to 55 characters
    message = ('%s %s'%(starter, logmessage))
    with open(smashinglog, "a") as myfile:
        myfile.write(message)
    if not logmessage2 == 'none':
        message = ('%s %s'%(starter, logmessage2))    
        with open(smashinglog, "a") as myfile:
            myfile.write(message)
        logmessage2 = 'none'
        if not logmessage3 == 'none':
            message = ('%s %s'%(starter, logmessage3))    
            with open(smashinglog, "a") as myfile:
                myfile.write(message)
            logmessage3 = 'none'
            if not logmessage4 == 'none':
                message = ('%s %s'%(starter, logmessage4))    
                with open(smashinglog, "a") as myfile:
                    myfile.write(message)
                logmessage4 = 'none'
                if not logmessage5 == 'none':
                    message = ('%s %s'%(starter, logmessage5))    
                    with open(smashinglog, "a") as myfile:
                        myfile.write(message)
                    logmessage5 = 'none'
                    
# errors
def errormessage():
    global error, error2, errornotification, logmessage, logmessage2, logmessage3, logmessage4, logmessage5
    print 'running errormessage()'
    printstar()
    logmessage = ('%s has stopped with an error'% thisaddon)
    print logmessage
    try:
        if not error == 'none':
            logmessage2 = error
            print error
    except:
        pass
    try:
        if not error2 == 'none':
            logmessage3 = error2
            print error2
    except:
        pass
    try:
        if not error3 == 'none':
            logmessage4 = error3
            print error3
    except:
        pass
    try:
        if not error3 == 'none':
            logmessage5 = error4
            print error3
    except:
        pass
    printlog()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    # try marker stuff - delete it if present, otherwise it will stop the script running next time
    if os.path.exists(MARKER):
        print ('MARKER exists at %s'% MARKER)
        try:
            os.remove(MARKER)
            if not os.path.exists(MARKER):
                print 'MARKER has been removed'
                xbmc.sleep(300)
        except:
            print ('The marker file (%s) could not be deleted'% MARKER)
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(Marker file - was not removed)')
    else:
        print ('No MARKER file to delete at %s'% MARKER)
    try:
        if not errornotification == 'none':
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(errornotification)')
    except:
        pass
    try:
        if not errordialogheader == 'none':
            xbmc.sleep(3000)
            xbmcgui.Dialog().ok(errordialogheader, *errordialoglist)    # need * to use with list or errors out
    except:
        pass
    printstar()
    exit()                    
                    
                    

# Run this first, so can define in terms of thisaddon:
def startaddon():
    global thisaddon, logmessage
    print 'running startaddon()'
    # check log exists
    if os.path.isfile(smashinglog):
        checklogsize()
    else:
        newsmashinglog()
    thisaddon = sys.argv[0]
    printstar()
    logmessage = '%s has started'% thisaddon
    print logmessage
    printlog()
    
# run startaddon() to generate thisaddon, so can continue
startaddon()
# define MARKER
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "%sisrunning.txt"% thisaddon)

getos()
	
# Get os
def getos():
    global platform, logmessage, logmessage2, error, host
    print 'running getos'
    host = socket.gethostname()
    if xbmc.getCondVisibility('system.platform.android'):
        platform = 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        platform = 'linux'
        if xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
            platform = 'libreelec'
        else:
            error = 'Platform identifies as linux but not as libreelec.'
            errormessage()
            
    elif xbmc.getCondVisibility('system.platform.windows'):
        platform = 'windows'
    else:
        error = 'Unable to identify the system platform.'
        errormessage()
    # log results:
    logmessage = ('Hostname is %s' % host)
    logmessage2 = ('You\'re using %s' % platform)
    printlog()

# def getoptions():
# select machine drives are on
# select which drives are being used
# select local or mysql library
# if mysql what machine is it on?
# select loglevel
# select cache option (zero or not)
def getoptions():
    global driveshost, driveshostip, drives, force, editcurrent, logmessage, logmessage2, error, error2, error3, error4, extranames, extradetails
    print 'running getoptions()'
    size = len(sys.argv)
    print ('size is %s'% size)
    if len(sys.argv) > 1:
        c = 1
        num = len(sys.argv)
        while c < num:
            d = sys.argv[c]
            if d[:14] == '<driveshost = ':
                driveshost = d[14:-1]
                print ('driveshost is %s'% driveshost)
                # check that's a valid option - either 'local' or does it appear in ipaddresses.xml?
                f = open(IPADDRESSES,"r")
                lines = f.readlines()
                length = len(lines)
                p = 0
                while p < length:
                    checkline = lines[p]
                    if driveshost in checkline:
                        begin = '<name = '
                        end = '>'
                        name = (checkline.split(begin))[1].split(end)[0]
                        start = '<IP = '
                        finish = '>'
                        IP = (checkline.split(start))[1].split(finish)[0]
                        if driveshost == name:
                            driveshostip = IP
                            p = length
                        elif driveshost = IP
                            driveshostip = IP
                            p = length
                        else:
                            logmessage = 'Problem in getoptions()'
                            logmessage2 = 'driveshost in argument was not valid (%s)'% driveshost
                            printlog()
                    p = p + 1   # if driveshostip is still 'false' it will be set in the gui    
            elif d[:10] == '<drives = ':
                drives = d[10:-1]
                print ('drives is %s'% drives)
                # check that's a valid option - does it appear in drivesource.xml?
                f = open(DRIVESOURCES,"r")
                lines = f.readlines()
                number = len(lines)
                q = 0
                while q < number:
                    checkline = lines[q]
                    if drives == checkline.strip():
                        driveschecked = 'true'
                        q = number
                    q = q + 1
            elif d == '<force>':
                force = 'true'
            elif d == '<editcurrent>':
                editcurrent = 'true'
            elif d == '<locallibrary>':
                locallibrary = 'true'
            elif d[:17] == '<mysqlhostname = ':
                mysqlhostname = d[17:-1]
                print ('mysqlhostname is %s'% mysqlhostname)
                # check that's a valid option - either 'local' or does it appear in ipaddresses.xml?
                if mysqlhostname == 'local':
                    mysqlipip = '127.0.0.1'
                else:
                    f = open(IPADDRESSES,"r")
                    lines = f.readlines()
                    length = len(lines)
                    p = 0
                    while p < length:
                        checkline = lines[p]
                        if mysqlhostname in checkline:
                            begin = '<name = '
                            end = '>'
                            name = (checkline.split(begin))[1].split(end)[0]
                            start = '<IP = '
                            finish = '>'
                            IP = (checkline.split(start))[1].split(finish)[0]
                            if mysqlhostname == name:
                            mysqlip = IP
                            mysql = 'true'
                            p = length
                        elif mysqlhostname = IP
                            mysqlip = IP
                            mysql = 'true'
                            p = length
                        else:
                            logmessage = 'Problem in getoptions()'
                            logmessage2 = 'mysql in argument was not valid (%s)'% mysql
                            printlog()
                    p = p + 1   # if mysqlip is still 'false' it will be set in the gui
            elif d[:11] == '<mysqlip = ':
                mysqlip = d[11:-1]
                mysqlhostname = mysqlip             # ip trumps name
                mysql = true
            elif d[:14] == '<mysql port = ':
                mysqlport = d[14:-1]
                print ('mysql port is %s'% mysqlport)
            elif d[:14] == '<mysql user = ':
                mysqluser = d[14:-1]
                print ('mysql user is %s'% mysqluser)
            elif d[:14] == '<mysql pass = ':
                mysqlpass = d[14:-1]
                print ('mysql pass is %s'% mysqlpass)
            elif d[:14] == '<mysql name = ':
                mysqlname = d[14:-1]
                print ('mysql name is %s'% mysqlname)
            elif d[:10] == '<setextra.':
                begin = '<name = '
                end = '>'
                extra = (checkline.split(begin))[1].split(end)[0]
                extralist = []
                extralist = extra.split(' ')
                # should be 2 items in the list, or generate error
                if not len(extralist) == 2:
                    error = 'Problem in getoptions()'
                    error2 = 'extralist is not valid - it should be 2 items with a space in-between.'
                    error3 = ('Problem extralist is %s'% extralist)
                    error4 = ('extralist was generated from argument: %s'% d)
                    errormessage
                s = extralist[0]
                t = extralist[1]
                extranames.append(s)
                extradetails.append(t)

            c = c + 1

def readexistingsettings():
    global logmessage, logmessage2, error, error2
    print 'running getexistingsettings()'
    test = []
    # openadvsettings, read bottom lines to identify
    if os.path.isfile(ADVANCEDSETTINGS):
        lines = file(ADVANCEDSETTINGS, 'r').readlines()
        num = len(lines)
        c = 0
        while c < num:
            checkline = lines[c]
            if checkline[:12] == '<!--setting.':
                begin = '<!--setting.'
                end = ' = '
                checksett = (checkline.split(begin))[1].split(end)[0]
                checksett = checksett.strip()
                start = ' = '
                finish = '-->'
                checksettvalue = (checkline.split(start))[1].split(finish)[0]
                checksettvalue = checksettvalue.strip()
                if checksett == 'host':
                    currenthost = checksettvalue
                elif checksett == 'platform':
                    currentplatform = checksettvalue
                elif checksett == 'driveshost':
                    currentdriveshost = checksettvalue
                elif checksett == 'driveshostip':
                    currentdriveshostip = checksettvalue
                elif checksett == 'mysql':
                    currentmysql = checksettvalue
                elif checksett == 'mysqlip':
                    currentmysqlip = checksettvalue
                    currentmysql = 'true'
                elif checksett == 'mysqluser':
                    currentmysqluser = checksettvalue
                elif checksett == 'mysqlpass':
                    currentmysqlpass = checksettvalue
                elif checksett == 'mysqlname':
                    currentmysqlname = checksettvalue
                elif checksett == 'extrasetting':
                    if currentextra1 == 'none':
                        currentmysqlname = currentextra1
                    
                  
                    
                    
                    
                elif checksett == 'platform':
                    currentplatform = checksettvalue
                elif checksett == 'platform':
                    currentplatform = checksettvalue
                elif checksett == 'platform':
                    currentplatform = checksettvalue
                    
                    
                    
                    
                    
                    
                    
                 
            
            
            elif checkline[:18] == '<!--endsettings-->':
                currentendsettings == 'true'
                c = num
            else:
                pass
            c = c + 1
        # check settings have a valid ending, generate a notification if not
        if currentendsettings == 'false':
            logmessage = 'Problem in readexistingsettings()'
            logmessage2 = 'No \'<!--endsettings-->\' tag found'
            yesnowindow = xbmcgui.Dialog().yesno('Existing advancedsettings.xml can not be read', 'Click yes to continue', 'This will remove your exising advanced settings')
            if not yesnowindow:
                error = 'Script cancelled by user'
                error2 = 'Check existing advancedsettings.xml for end tag'
                errormessage()
            else:
                # get new settings
                getnewsettings()

                






                
def getnewsettings():
    global 
    print 'running getnewsettings()'
    
    
    
def queries():
    global host, driveshost, drives, error, error2, error3, error4, default, msg, input, checkline, default, name, defaultpath, EXTRA, extradefault, extradefaultdescription
    print 'running queries()'
    if not driveshost:
        # make a list of the possible options
        driveshostlist = []
        f = open(IPADDRESSES, "r")
            lines = f.readlines()
            num = len(lines)
            c = 0
            driveshostlist.append('on this machine (local drives)')
            while c < num:
                g = lines[c]
                # clean g to get just hostnames - lose ip addresses and spaces
                sep = '<'
                g = g.split(sep, 1)[0]
                g = g.strip()                
                if not g = host:
                    driveshostlist.append(g)
                c = c + 1
            driveshostlist.append('on a different machine')
        # ask the question
        CHOOSE = xbmcgui.Dialog().select("Where are your drives?", driveslisthost)
        CHOICE = driveslisthost[CHOOSE]
        if CHOOSE == -1:
            error = 'Script cancelled by user'
            error2 = 'Problem in queries() getting driveshost'
            errormessage()
        driveshost = driveslisthost[CHOOSE]
        # now need to get driveshostip
        if driveshost == 'on this machine (local drives)':
            driveshost = host
        elif driveshost == 'on a different machine':
            # input ip of driveshost manually
            keyboard = xbmc.Keyboard("", "Enter hostname or IP", False)
            keyboard.doModal()
            if keyboard.isConfirmed() and keyboard.getText() != "":
                driveshost = keyboard.getText()
                # treat as driveshost and driveshostip
                driveshostip = driveshost     
        if not driveshostip:
            f = open(IPADDRESSES, "r")
                lines = f.readlines()
                num = len(lines)
                c = 0
                while c < num:
                    k = lines[c]
                    if host in k:
                        begin = "<"
                        end = ">"
                        driveshostip = (checkline.split(begin))[1].split(end)[0]
                        c = num
                    c = c + 1
                if not driveshostip:
                    error = 'Problem in queries() getting driveshostip'
                    errormessage()
                    

    if not drives:
        # make a list of the possible options
        driveslist = []
        f = open(DRIVESOURCES, "r")
        lines = f.readlines()
        num = len(lines)
        c = 0
        while c < num:
            g = lines[c]
            g = g.strip()
            if not g[-5:] == 'local':
                driveslist.append(g)
            else:
                checkhost = g[:-5]
                if host == checkhost:
                    driveslist.append(g)
            c = c + 1
        # ask the question
        CHOOSE = xbmcgui.Dialog().select("Which drives do you want to use?", driveslist)
        CHOICE = driveslist[CHOOSE]
        if CHOOSE == -1:
            error = 'Script cancelled by user'
            error2 = 'Problem in queries() getting driveshost'
            errormessage()
        drives = driveslist[CHOOSE]
        if not drives:
            error = 'Problem in queries() getting drives'
            errormessage()
            
    if not locallibrary:
        if not mysql:
            # ask the question
            local = 'A local library on this machine'
            remote = 'A mysql library'
            none = 'Don\'t use a library'
            CHOOSE = xbmcgui.Dialog().select("What type of library do you want?", local, remote, none)
            if CHOOSE == 'local':
                locallibrary = 'true'
            elif CHOOSE == 'remote':
                mysql = 'true'
            elif CHOOSE = 'none':
                nolibrary = 'true'
            else:
                error = 'Script cancelled by user'
                error2 = 'Problem in queries() getting library type'
                errormessage()
            
    if mysql = 'true':
        # Are mysqlname / mysqlip known?
        if not mysqlip:
            # build list of possible hosts
            listmachines = []
            listnames = []
            listips = []
            localmachine = ('This machine (%s)'% host)
            othermachine = 'Choose a different machine'
            listmachines.append(localmachine)
            listnames.append(host)
            f = open(IPADDRESSES, "r")
            lines = f.readlines()
            num = len(lines)
            c = 0
            while c < num:
                checkline = lines[c]
                sep = '<'
                name = checkline.split(sep, 1)[0]
                name = name.strip()
                begin = "<"
                end = ">"                    
                IP = (checkline.split(begin))[1].split(end)[0]
                if host not in checkline:
                    addmachine = ('%s (%s)'% (name, IP)
                    listmachines.append(addmachine)
                else:
                    listips.insert(0,IP)
                c = c + 1
            listmachines.append(othermachine)
            listnames.append(othermachine)
            listips.append(othermachine)
            # check host is in IPADDRESSES
            if not len(listmachines) = len(listips):
                error = 'problem in queries()'
                error2 = ('listmachines and listips lists are different lengthes - is host (%s) in IPADRESSES (%s)?'% (host, IPADDRESSES))
                error3 = ('listmachines is %s'% listmachines)
                error4 = ('listips is %s'% listips)
                errormessage()
            # ask the question
            CHOOSE = xbmcgui.Dialog().select("Where is the mysql database located?", listmachines)
            CHOICE = listmachines[CHOOSE]
            if CHOOSE == -1:
                error = 'Script cancelled by user'
                error2 = 'Problem in queries() getting mysql machine'
                errormessage()
            mysqlname = listnames[CHOOSE]
            mysqlip = listips[CHOOSE]
            if mysqlname == othermachine:
                # manual input:
                keyboard = xbmc.Keyboard("", "Enter host name or IP", False)
                keyboard.doModal()
                if keyboard.isConfirmed() and keyboard.getText() != "":
                    mysqlname = keyboard.getText()
                    # treat as mysqlname and mysqlip
                    mysqlip = mysqlname
                else:
                    error = 'Problem with mysqlname keyboard input in queries()'
                    error2 = 'Script cancelled by user'
                    errormessage()
                    
        # Go over rest of mysql settings
        if not mysqlport:
            variable = mysqlport
            getdefault()
            mysqlport = default
        if not mysqluser:
            variable = mysqluser
            getdefault()
            mysqluser = default
        if not mysqlpass:
            variable = mysqlpass
            getdefault()
            mysqlpass = default
        if not mysqlname:
            variable = mysqlname
            getdefault()
            mysqlname = default
        r = 0
        while r < 20        # 20 = arbitrary value
            
            # make list for dialogselect:
            if not mysqlname == mysqlip:
                a = ('mysql database on %s (IP %s)'% (mysqlhostname, mysqlip))
            else:
                a = ('mysql database on %s'% mysqlip)
            b = ('mysql port = %s'% mysqlport)
            c = ('mysql username = %s'% mysqluser)
            d = ('mysql password = %s'% mysqlpass)
            e = ('mysql database name = %s'% mysqlname)
            f = 'All settings correct. Continue.'
            g = 'Cancel script'
            sqlstuff = []
            sqlstuff.append(a,b,c,d,e)
            if mysqlhostname:
                if mysqlip:
                    if mysqluser:
                        if mysqlpass:
                            if mysqlname:
                                sqlstuff.append(f)
            sqlstuff.append(g)
            CHOOSE = xbmcgui.Dialog().select("Check mysql settings", sqlstuff)
            CHOICE = sqlstuff[CHOOSE]
            if CHOICE == a:
                msg = 'Enter mysql location (host name or IP)'
                querymysql()
                mysqlip = input
            elif CHOICE == b:
                msg = 'Enter value for mysql port'
                querymysql()
                mysqlport = input
            elif CHOICE == c:
                msg = 'Enter mysql username'
                querymysql()
                mysqluser = input
            elif CHOICE = d:
                msg = 'Enter mysql password'
                querymysql()
                mysqlpass = input
            elif CHOICE = e:
                msg = 'Enter mysql database name'
                querymysql()
                mysqlname = input
            elif CHOICE = f:
                r = 25      # arbitrary value > 20
            elif CHOICE = g:
                error = 'Problem confirming sql settings in queries()'
                error2 = 'Script cancelled by user - selected \'Cancel script\' option.'
                errormessage()
            else:
                error = 'Problem confirming sql settings in queries()'
                error2 = 'Script cancelled by user'
                errormessage()
            r = r + 1
        if r < 25:
            error = 'Problem in queries'
            error2 = 'Not all mysql variables have been given a value'
            errormessage()
            
    # extra settings now
    # check pathsubs.xml for anything with <default>; list these, select to change - if change select from options in pathsubs.xml or add own
    # check defaultvalues.xml - go through as above
    r = 0
    while r < 20        # 20 = arbitrary value
            
        # make list for dialogselect:
        EXTRA = 'false'
        extras = []
        defaultpaths = []
        defaultpathsdescriptions = []
        listentries = []
        # add entries to lists
        f = open(PATHSUBS, "r")
        lines = f.readlines()
        num = len(lines)
        c = 0
        while c < num:
            checkline = lines[c]
            if '<default>' in checkline:
                checkdefaultpath()
                if defaultpath:
                    listentry = ('%s is set to %s'% (name, defaultpathdescription)
                    extras.append(name)
                    defaultpaths.append(defaultpath)
                    defaultpathsdescriptions.append(defaultpathdescription)
                    listentries.append(listentry)
            c = c + 1
        # add entries to lists
        cont = 'Accept all values and continue'
        cncl = 'Cancel script'
        listentries.append(cont,cncl)
        # ask
        CHOOSE = xbmcgui.Dialog().select("Click an entry to change the setting", listentries)
        CHOICE = listentries[CHOOSE]
        if CHOICE == cncl:
            error = 'Problem in queries - adding extra path settings'
            error2 = 'Script cancelled by user - user selected cncl'
            errormessage()
        elif CHOOSE == -1:
            error = 'Problem in queries() - adding extra path settings'
            error2 = 'Script cancelled by user'
            errormessage()
        elif CHOICE == cont:
            r = 25
        # process chosen extra
        EXTRA = extras[CHOOSE]
        extradefault = defaultpaths[CHOOSE]
        extradefaultdescription = defaultpathsdescriptions[CHOOSE]
        queryextrapath()
        
        
    
    
        

def getdefault():
    global variable, default, logmessage, logmessage2
    print 'running getdefault()'
    f = open(DEFAULTS, "r")
    lines = f.readlines()
    num = len(lines)
    c = 0
    default = 'not set'
    while c < num:
        checkline = lines[c]
        sep = '<'
        value = checkline.split(sep, 1)[0]
        value = value.strip()
        if value == variable:
            begin = "<"
            end = ">"                    
            default = (checkline.split(begin))[1].split(end)[0]
            c = num
        c = c + 1
    if default == 'not set':
        logmessage = 'problem in getdefault()'
        logmessage2 = ('No default value found for variable (%s)'% variable)
        printlog()

def querymysql():
    global error, error2, msg, input
    print 'running querymysql()'
    keyboard = xbmc.Keyboard("", msg, False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        input = keyboard.getText()

# parse pathsubs.xml to generate list of alternatives        
def checkdefaultpath():
    global name, defaultpath, defaultpathdescription
    print 'running checkdefaultpath()'
    name = 'false'
    defaultpath = 'false'
#    alternatives = 'false'         # not needed - only need to establish the default
#    alt = []                       # not needed - only need to establish the default and if more than 1 option exists
    if '<name>' in checkline:
        begin = '<name = '
        end = '>'
        name = (checkline.split(begin))[1].split(end)[0]
        if '<default>' in checkline:
            begin = '<default>'
            end = '</default>'
            defaultpath  = (checkline.split(begin))[1].split(end)[0]
        specific = '<' + host + '.' + platform + '>'
        if specific in checkline:
            specend = '</' + host + '.' + platform + '>'
            start = specific
            finish = specend
            defaultpath = (checkline.split(start))[1].split(finish)[0]       # overrides usual defaultpath
#            alternatives = 'true'
#        elif '<option>' in checkline:
#            if not '<option></option>' in checkline:            # ie if not empty
#                alternatives = 'true'
    # if defaultpath exists get the text to display in options dialog
    if defaultpath:
        print ('defaultpath is %s'% defaultpath)
        sep = '['
        defaultpathdescription = text.split(sep, 1)[0]
        defaultpathdescription = defaultpath.strip()
        print ('defaultpathdescription is %s'% defaultpathdescription)
        start = '['
        finish = ']'
        defaultpath = (defaultpath.split(start))[1].split(finish)[0]
        defaultpath = defaultpath.strip()
   
        
def queryextrapath():
    global error, error2, msg, EXTRA, extrapath
    print 'running queryextrapath()'
    options = []
    default = 'false'
    olddefault = 'false'
    f = open(PATHSUBS, "r")
    lines = f.readlines()
    num = len(lines)
    c = 0
    while c < num:
        checkline = lines[c]
        if EXTRA in checkline:
            # process line, get all available options
            if '<default>' in checkline:
                begin = '<default>'
                end = '</default>'
                default  = (checkline.split(begin))[1].split(end)[0]
            specific = '<' + host + '.' + platform + '>'
            if specific in checkline:
                olddefault = default
                specend = '</' + host + '.' + platform + '>'
                start = specific
                finish = specend
                default = (checkline.split(start))[1].split(finish)[0]
            if default:
                defaultmessage = ('Default is %s'% default)
                options.append(defaultmessage)
                if olddefault:
                    options.append(olddefault)
            # now look for others
            d = 0
            while d < 10:                   # arbitrary
                if '<option' in checkline:
                    begin = '<option'
                    end = '</option>'
                    test  = (checkline.split(begin))[1].split(end)[0]
                    if test[:1] = '.':
                        test = test[1:]
                        check = test.split('>')[0]       # split > list, [0] > 1st item
                        if check = host:                # include in list
                            begin = '>'
                            end = '</option>'
                            option = (test.split(begin))[1].split(end)[0]
                            options.append(option)
                    elif test[:1] = '>':
                        begin = '>'
                        end = '</option>'
                        option = (test.split(begin))[1].split(end)[0]
                        options.append(option)
                    else:
                        error = 'Problem in queryextrapath()'
                        error2 = 'Cannot process extra options'
                        errormessage()
                    d = d + 1
                else:
                    d = 10
        c = c + 1
    enter = 'Enter a new path'
    options.append(enter)
    cncl = 'Cancel script'
    options.append(cncl)
    CHOOSE = xbmcgui.Dialog().select("Choose option:", options)
    CHOICE = options[CHOOSE]
    if CHOICE == cncl:
        error = 'Script stopped in queryextrapath()'
                error2 = 'Script cancelled by user - selected \'Cancel script\' option.'
                errormessage()
    elif CHOICE == enter:
        txt = 'Enter the new path'
        keyboard = xbmc.Keyboard("", txt, False)
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText() != "":
            newpath = keyboard.getText()    
    elif CHOICE = defaultmessage:
        start = '['
        finish = ']'
        newpath = (default.split(start))[1].split(finish)[0]
        newpath = default.strip()    
    else:
                                
                    

            
        
        
# Drink beer