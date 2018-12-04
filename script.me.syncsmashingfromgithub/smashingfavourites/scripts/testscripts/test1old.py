# -*- coding: utf-8 -*-
import xbmc
import os
import shutil
# backup database folder
# remove old database versions

# -*- coding: utf-8 -*-
import xbmc
import os
import shutil
# backup database folder
# remove old database versions

# define some places
USERDATA = xbmc.translatePath('special://masterprofile')
DATABASEFOLDER = os.path.join(USERDATA, "Database")
DATABASEBACKUP = os.path.join(USERDATA, "Databasebackups")
# path to advancedsettings options folders:	
FOLDERSPATH = os.path.join(USERDATA, "advancedsettings")
# path to working advancedsettings.xml
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")

# Check what's running now
# Open file, read details
def getadvancedsettings():
    if os.path.isfile(ADVANCEDSETTINGS):
    # count lines in file
        with open(ADVANCEDSETTINGS) as foo:
            length = len(foo.readlines())
        lines = file(ADVANCEDSETTINGS, 'r').readlines()
        print ('length= %s' % length)
        # 1 line up
        length = length - 2
        print ('length= %s' % length)
        k = lines[length].rstrip()
        printstar()
        print ('k = %s' % k)
        if k == 'platform:':
            plat = lines[-1].rstrip()
        else:
            problem = 'platform'
            checkxml()
        # 3 lines up
        length = length - 2
        k = lines[length].rstrip()
        if k == 'drives:':
            pos = length + 1
            j = lines[pos]
            drives = j.rstrip()
        else:
            problem = 'drives'
            checkxml()
        # 5 lines up
        length = length - 2
        k = lines[length].rstrip()	
        if k == 'localormysql:':
            localormysqldatabase = lines[-5].rstrip()
        else:
            problem = 'localormysqldatabase'
            checkxml()
        # 7 lines up
        length = length - 2
        k = lines[length].rstrip()
        if k == 'source machine:':
            source = lines[-7].rstrip()
        else:
            problem = 'source'
            checkxml()
        # 9 lines up
        length = length - 2
        k = lines[length].rstrip()
        if k == '		<loglevel>1</loglevel>':			
            debug = 'enabled'
        elif k == '		<loglevel>0</loglevel>':
            debug == 'not enabled'
        else:
            problem = 'debug'
            checkxml()
        printstar()
        print ('Currently using %s' % drives)
        print ('Database is %s' % localormysqldatabase)
        print ('The drives are located on %s' % source)
        print ('Debug logging - %s' % debug)
        printstar()
    else:
        printstar()
        print 'No advancedsettings.xml file is in place.'


#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# Stop if problems with existing advancedsettings.xml
def checkxml():
    printstar()
    print 'There is a problem with the existing advancedsettings.xml'
    print 'It does not follow the needed format in the end lines.'
    print 'Sort it out and try again.'
    print ('The first problem found is with %s' % problem)
    printstar()
    exit()

# Get hostname
def host():
    host = socket.gethostname()
	
# Get os
def getos():
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
    # log
    printstar()
    print 'Starting advancedsettings.py'
    print ('Hostname is %s' % host)
    print ('You\'re using %s' % PLATFORM)
    printstar()

def listoptions():
    # Make a list of the available options:
    ADVSETTS = []
    for i in os.listdir(FOLDERSPATH):
        if os.path.isdir(os.path.join(FOLDERSPATH,i)):
    # openadvsettings, read bottom lines to identify
            TARGETFILE = os.path.join(FOLDERSPATH,i,'advancedsettings.xml')
            if os.path.isfile(TARGETFILE):
#            if os.path.isfile(os.path.join(FOLDERSPATH,i,'advancedsettings.xml')):
                lines = file(TARGETFILE, 'r').readlines()
                test = lines[-1]
                printstar()
                print ("test returns as %s" % test)
                printstar()
                if test == PLATFORM or test == 'all':			
                    ADVSETTS.append(i)
    n = len(ADVSETTS)
    print ("There are %d available advancedsettings options." % n)
    if n == 0:
        printstar()
        print "No advanced settings available"
        printstar()
        exit()
	
def chooseadvancedsettings():
    # Display list and get choice
    CHOOSE = xbmcgui.Dialog().select("Options", ADVSETTS)
    CHOICE = ADVSETTS[CHOOSE]
    printstar()
    print ("Choice = %s" % CHOICE)
    printstar()
    NEWADVSETTS = os.path.join(FOLDERSPATH, CHOICE, "advancedsettings.xml")
    if os.path.isfile(NEWADVSETTS):
        os.remove(ADVANCEDSETTINGS)
        shutil.copy(NEWADVSETTS, USERDATA)
        printstar()
        print "New advanced settings loaded"
        printstar()
    exit()	
	
def backupdatabase():
    # make backup folder if not there already
    if not os.path.exists(DATABASEBACKUP):
        os.mkdir(DATABASEBACKUP)
#        printstar()
#        print 'Databasebackups folder created'
#        printstar()
    # copy contents of database folder into database backup folder (overwrite if already present).
    for i in os.listdir(DATABASEFOLDER):
        s = os.path.join(DATABASEFOLDER, i)
        d = os.path.join(DATABASEBACKUP, i)
        if os.path.isfile(s):
            shutil.copy(s, d)

def removeolddatabases():
    # Make a list of database folder contents
    #global DBLIST
    #global DBDUPS
    #global DUPS
    DBLIST = []
    DBDUPS = []
    DUPS = []
    for i in os.listdir(DATABASEFOLDER):
        if os.path.isfile(os.path.join(DATABASEFOLDER,i)):
            TARGETFILE = os.path.join(DATABASEFOLDER,i)
            if os.path.isfile(TARGETFILE):
                # strip numbers, strip .db from end
                k = ''.join(q for q in i if not q.isdigit())
                l = k[:-3]
                DBDUPS.append(l)
                DBLIST.append(i)	
# Check DBDUPS for duplicate entries
    #[x for x in mylist if mylist.count(x) >= 2]
    for x in DBDUPS:
        if DBDUPS.count(x) >= 2 and DUPS.count(x) == 0:
            DUPS.append(x)	
# Remove old databases
# Add all duplicates to DEL list
# Identify largest number for each duplicate
# rebuild file name and remove from DEL
# delete files left in DEL	
    DEL = []
    if len(DUPS) != 0:
        for i in DUPS:
            for j in DBLIST:
                k = ''.join(q for q in j if not q.isdigit())
                l = k[:-3]
#                printstar()
#                print 'Here they come, i and l'
#                print i
#                print l
                if i == l:
                    DEL.append(j)
#        print ('DEL = %s' % DEL)
        x = len(DUPS)
        y = len(DEL)
        #print ('x = %d' % x)
        #print ('y = %d' % y)
        c = 0
        SIZE = []
        KEEP = []
        while c < x:
            check = DUPS[c]
            #print ('c = %d' % c)
            #print ('DUPS[%d] = %s' % (c, DUPS[c]))
            c = c + 1
            for z in range(0, y):
                k = DEL[z]
#                print ('DEL[%d] = %s' % (z, DEL[z]))
                l = ''.join(q for q in k if not q.isdigit())
                m = l[:-3]
#                print ('m = %s' % m)
                if m == check:
                    n = ''.join(r for r in k if r.isdigit())
                    n = int(n)
                    SIZE.append(n)
                    #print ('SIZE = %s' % SIZE)
            LATEST = max(SIZE)
            LATEST = str(LATEST)
            SAVEDB = ('%s%s.db' % (check, LATEST))
            KEEP.append(SAVEDB)
            #print ('Database to save is %s' % SAVEDB)			
            del SIZE[:]
        #print ('Files to keep from duplicates are: %s' % KEEP)
        c = 0
        y = len(KEEP)
        while c < y:
            z = KEEP[c]
            c = c + 1
            if z in DEL:
                DEL.remove(z)
                #print ("Database to keep: %s" % z)
        #print ('Files to really delete: %s' % DEL)
        # Do the biz
        for i in DEL:        		
            if os.path.isfile(os.path.join(DATABASEFOLDER,i)):
                os.remove(os.path.join(DATABASEFOLDER,i))
                print ('Database file(%s) deleted' % i)
				
 
 
 
backupdatabase()
removeolddatabases()

#printstar()
#print ('DBLIST = %s' % DBLIST)
#print ('DBDUPS = %s' % DBDUPS)
#print ('DUPS = %s' % DUPS)
#exit()











# Drink beer