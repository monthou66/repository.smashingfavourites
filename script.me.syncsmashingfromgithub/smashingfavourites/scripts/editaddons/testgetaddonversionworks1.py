# -*- coding: utf-8 -*-
# testgetaddonversion.py


import xbmc
import xbmcaddon
import os

error = 'non-specific'
addon_id = 'not found'
clone_id = 'not found'
addon_path = 'not found yet'
addon_version = 'not found yet'
xml = 'not found yet'
error = 'non-specific'

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
    global addon_id, clone_id
    if len(sys.argv) > 1:
        addon_id = sys.argv[1]
    if len(sys.argv) > 2:
        clone_id = sys.argv[2]
    if len(sys.argv) > 3:
        if sys.argv[3] == 'force':
            startclone()

    
    
    
def getaddonid():
    global source, addon_path, addon_version
    source = 'Results from xbmcaddon.getAddonInfo:'
# only works if addon is enabled
    if xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id):
        addon         = xbmcaddon.Addon(id='%s'% addon_id)
        addon_path    = addon.getAddonInfo('path')
        addon_version = addon.getAddonInfo('version')

def getaddonpath():
    global source, addon_path, addon_version
    source = 'Results from looking for folders:'
    addon = 'pvr.iptvsimple'
    addon_path = 'not found yet'
    addon_version = 'not found yet'    
    checkpath = os.path.join(xbmc.translatePath('special://home/addons/%s'% addon))
    alternatepath = os.path.join(xbmc.translatePath('special://xbmc/addons/%s'% addon))
    if os.path.exists(alternatepath):
        addon_path = alternatepath
    elif os.path.exists(checkpath):
        addon_path = checkpath
        
def getaddonversionfromxml():     
    global source, addon_path, addon_version, xml
    source = 'Results from reading addon.xml:'  
    
    # check 1
#    print ('check 1: addon_path is %s'% addon_path)

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
    
def startclone():
    print 'running startclone'
    exit()    
    
startaddon()
getarguments()
if addon_id == 'not found':
    error = 'No addon_id to check'
    errormessage()
getaddonid()
output()
getaddonpath()
output()
getaddonversionfromxml()
output()
if clone_id == 'not found':
    error = 'No clone_id to check'
    errormessage()
addon_id = clone_id
getaddonid()
output()
getaddonpath()
output()
getaddonversionfromxml()
output()
exit()

# Drink beer



