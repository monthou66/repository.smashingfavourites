# -*- coding: utf-8 -*-
# testgetaddonversion.py


import xbmc
import xbmcaddon
import os
import shutil

# define some places:
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))        # this is the read-only default folder
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))               # addons are normally installed in this folder
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONS = os.path.join(MISC, "addons")
OLDADDONS = os.path.join(SMASHINGADDONS, "oldaddons")




addon_id = 'not found'
clone_id = 'not found'
addon_path = 'not found yet'
addon_version = 'not found yet'
xml = 'not found yet'
error = 'non-specific'
force_clone = 'false'

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def errormessage():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    if not error == 'non-specific':
        print error
    printstar()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)
    exit()

def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

def getarguments():
    global addon_id, donor_id, clone_id, force_clone, error
    if len(sys.argv) > 3:
        donor_id = sys.argv[1]
        clone_id = sys.argv[2]
        clone_name = sys.argv[3]
    else:
        error = 'Not enough arguments'
        errormessage()
    if len(sys.argv) > 4:
        if sys.argv[4] == 'force':
        # check
            print sys.argv[4]
            force_clone = 'true'
            print ('force_clone is %s'% force_clone)
    
def getaddonpathandversion():
    global source, addon_path, addon_version, xml
    source = 'Results from xbmcaddon.getAddonInfo:'
# only works if addon is enabled
    if xbmc.getCondVisibility('System.HasAddon(%s)' % check):
        addon         = xbmcaddon.Addon(id='%s'% check)
        addon_path    = addon.getAddonInfo('path')
        addon_version = addon.getAddonInfo('version')
        addon_name    = addon.getAddonInfo('name')
        addon_author    = addon.getAddonInfo('author')
        addon_summary    = addon.getAddonInfo('summary')
        addon_disclaimer    = addon.getAddonInfo('disclaimer')
        xml = os.path.join(addon_path, 'addon.xml')
        output()
    else:
        getaddonpathandversionfromxml()

def getaddonpathandversionfromxml():
    global source, addon_path, addon_version, xml, error, clone_exists
    source = 'Results from looking for folders and reading addon.xml:'
    addon_path = 'not found yet'
    addon_version = 'not found yet'    
    checkpath = os.path.join(ADDONSFOLDER, check)      # addons are normally installed in this folder
    alternatepath = os.path.join(DEFAULTADDONSFOLDER, check)  # this is the read-only default folder
    if os.path.exists(checkpath):
        addon_path = checkpath
    elif os.path.exists(alternatepath):
        addon_path = alternatepath
# check this - shouldn't apply to clone!
    else:
        if check == donor_id:
            error = ('Addon path not found for %s'% check)
            errormessage()
        elif check == clone_id:
            clone_exists = 'false'
            output()
        else:
            error = 'check not recognised'
            errormessage()
        
    if not addon_path == 'not found yet':
        xml = os.path.join(addon_path, 'addon.xml')

        with open(xml, 'r') as myfile:
            lines = myfile.readlines()
            checkline = lines[2]
#            print ('checkline is %s'% checkline)
            if 'version' in checkline:
                start = 'version="'
                end = '"'           
                addon_version = (checkline.split(start))[1].split(end)[0]
                output()
            else:
                error = ('Could not get addon version')
                errormessage()

def output():    
    printstar()
    print source
    print ('path is %s'% addon_path)
    print ('version is %s'% addon_version)
    if not xml  == 'not found yet':
        print ('addon.xml is located at %s'% xml)
#    print 'json_query is:'
#    print json_query
    printstar()
    
def removeolddlls():
    global OLDDLLSTODELETE
    OLDDLLSTODELETE = os.path.join(OLDADDONS, "temp", clone_id)
    if not os.path.exists(OLDDLLSTODELETE):
        os.makedirs(OLDDLLSTODELETE)
        identifytempfolder()
    c = 1
    while c < 20:        
        num = str(c)
        OLDCLONEFOLDER = os.path.join(OLDDLLSTODELETE, num)
        if os.path.exists(OLDCLONEFOLDER):
            try:
                os.remove(OLDCLONEFOLDER)
                if not os.path.exists(OLDCLONEFOLDER):
                    print ('%s folder has been deleted'% OLDCLONEFOLDER)
                else:
                    print ('Failed to delete %s folder'% OLDCLONEFOLDER)
            except:
                print ('Failed to delete %s folder'% OLDCLONEFOLDER)
        else:
            print ('No folder found at %s'% OLDCLONEFOLDER)
        c = c + 1
    identifytempfolder()

def identifytempfolder():
    global FOLDER
#    temp = 1
    c = 1
    while c < 20:
        temp = str(c)
        FOLDER = os.path.join(OLDDLLSTODELETE, temp)
        if os.path.exists(FOLDER):
#            temp = temp + 1
            c = c + 1
        else:
            c = 20
    print ('temp folder is %s'% FOLDER)
    deleteoldclone()
    
def deleteoldclone():
    global FOLDER, error, OLDCLONE, OLDCLONEDLL
    OLDCLONE = os.path.join(OLDADDONS, clone_id)
    OLDCLONEDLL = os.path.join(OLDCLONE, '%s.dll'% clone_id)
    if os.path.exists(OLDCLONE):
        try:
            shutil.rmtree(OLDCLONE)
        except:
            if os.path.exists(OLDCLONEDLL):
                if not os.path.exists(FOLDER):
                    os.makedirs(FOLDER)
                    MOVED = os.path.join(FOLDER, '%s.dll'% clone_id)
                try:
                    os.rename(OLDCLONEDLL, MOVED)
                    if os.path.exists(MOVED):
                        try:
                            shutil.rmtree(OLDCLONE)
                        except:
                            error = ('Cannot delete %s'% OLDCLONEDLL)
                            errormessage()
                except:
                    error = ('Cannot delete %s'% OLDCLONEDLL)
                    errormessage()
    deletetempfolder()

def deletetempfolder():
    if os.path.exists(OLDDLLSTODELETE):
        try:
            shutil.rmtree(OLDDLLSTODELETE)
            print ('%s folder deleted'% OLDDLLSTODELETE)
        except:
            print ('%s folder could not be deleted.'% OLDDLLSTODELETE)
    moveclonetooldclone()
    
def moveclonetooldclone():
  if os.path.exists(clone_path):
      try:
          shutil.move(clone_path, OLDCLONE)
      except:
          xbmc.sleep(300)
          try:
              shutil.move(clone_path, OLDCLONE)
          except:
              error = ('Cannot move %s folder to %s'% (clone_path, clone_path))
              errormessage()
  startclone()    
    
def startclone():
    # copy donor addon to clone folder:
    print 'running startclone'
    xbmc.executebuiltin('Action(UpdateLocalAddons)')
    xbmc.sleep(300) 
    shutil.copytree(donor_path, clone_path)
    # start editing:
    # Work through all files in the folder.  If they end in .py or .xml do a substitution - clone_id for donor_id.
    # Extras - addon.xml: change addon name, change provider, don't change .dll referred to if binary addon
    testlistdir()
    
def testlistdir():
    global file, filepath
    testpath = os.path.join(ADDONSFOLDER, 'skin.xonfluence')
    list = os.listdir(testpath)
    printstar()
    print 'top level of skin.xonfluence folder:'
    for d in list:
        print d
    print 'Files in top level:'
    for d in list:
        e = os.path.join(testpath, d)
        if os.path.isfile(e):
            print e
    print 'Folders in top level:'
    for d in list:
        e = os.path.join(testpath, d)
        if os.path.isdir(e):
            print e
            
    # testing
    file = 'addon.xml'
    filepath = os.path.join(ADDONSFOLDER, clone_id, 'addon.xml')
    editaddonxml()
    
def selectfiles():
    global file, filepath
    if file == 'addon.xml':
        editaddonxml()
    elif file == 'addon.xml.in':
        editaddonxml()
    elif file[-3:] == 'xml':
        editfile()
    elif file[-2:]  == 'py':
        editfile()
    
def editaddonxml():
    global file, filepath
    # Replace variables in file
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(donor_id, clone_id))    
    # Don't rename .dll 9so change back here!):
    newdllname = ('%s.dll'% clone_id)
    olddllname = ('%s.dll'% donor_id)    
    with open(filepath, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(newdllname, olddllname))
    # get name of donor:
    exit()






        
def finish():
    printstar()
    print message
    printstar()
    exit()
    
startaddon()
getarguments()
# process donor addon:
if donor_id == 'not found':
    error = 'No addon_id to check'
    errormessage()
check = donor_id
getaddonpathandversion()
donor_path = addon_path
donor_version = addon_version
donor_xml = xml
# process clone addon:
check = clone_id
getaddonpathandversion()
clone_path = addon_path
if clone_path == 'not found yet':
    clone_path = os.path.join(xbmc.translatePath('special://home/addons/%s'% clone_id))
    print ('clone_path is %s'% clone_path)
clone_version = addon_version
clone_xml = xml
if clone_xml == 'not found yet':
    clone_xml = os.path.join(xbmc.translatePath('special://home/addons/addon.xml'))
    print ('clone_path is %s'% clone_path)
# if versions match there's nothing to do:
if not force_clone == 'true':
    if donor_version == clone_version:
        message = ('%s and %s are both version %s.  No need to update'% (donor_id, clone_id, donor_version))
        finish()
# Get rid of any existing backups and move existing addon into backup folder:
if os.path.exists(clone_path):
    removeolddlls()
else:
    startclone()
printstar()
print 'All done'
printstar()
# make new clone:
        
        
        
        
        
# Drink beer



