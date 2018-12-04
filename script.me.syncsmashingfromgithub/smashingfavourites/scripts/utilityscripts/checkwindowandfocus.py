#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcvfs

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
def printscript():
    print "Running checkwindowandfocus.py"	

def get_installedversion():
    global json_query, version
    # retrieve current installed version
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    # response is eg >> json_query is {"id":1,"jsonrpc":"2.0","result":{"name":"Kodi","version":{"major":17,"minor":4,"revision":"20170717-b22184d","tag":"releasecandidate","tagversion":"1"}}}
    start = 'major":'
    finish = ',"minor'
    version = (json_query.split(start))[1].split(finish)[0]
#    json_query = jsoninterface.loads(json_query)
#    version_installed = []
#    if json_query.has_key('result') and json_query['result'].has_key('version'):
#        version_installed  = json_query['result']['version']
#    return version_installed
	
# check open window and focus - need to know whether favourites sideblade is open / whether to move focus if in a list
name = xbmc.getInfoLabel('currentwindow')
win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
focus = win.getFocusId()
control = xbmc.getInfoLabel('System.CurrentControl')
#try:
dialog = xbmcgui.getCurrentWindowDialogId()
# check if favourites window is visible - no returns 0, yes returns 1
vis = xbmc.getCondVisibility('Window.IsVisible(10134)')
if vis == 1:
    fav = ""
else:
    fav = "not"
if len(sys.argv) > 1:
    sarg = sys.argv[1]
    print ('sys.argv[1] is %s'% sarg)
    if sarg == 'back' or 'Back':
        xbmc.executebuiltin( "XBMC.Action(Back)" )
        xbmc.executebuiltin( "XBMC.Action(Left)" )
        xbmc.executebuiltin( "XBMC.Action(Right)" )
        print 'going back'
        xbmc.sleep(1000)
name = xbmc.getInfoLabel('currentwindow')
win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
window = xbmcgui.getCurrentWindowId()
focus = win.getFocusId()
control = xbmc.getInfoLabel('System.CurrentControl')	

# get Container.FolderPath and Container.FolderName 
FolderPath = xbmc.getInfoLabel('Container.FolderPath')
FolderName = xbmc.getInfoLabel('Container.FolderName')

# add question for pvr working or not
pvrloading = xbmc.getCondVisibility('Window.IsVisible(10151)')
if pvrloading == 1:
    pvrloading = ""
else:
    pvrloading = "not"
    
# get a list of running addons
running = xbmcvfs.listdir('addons://running/')[1]   
num = len(running)

# get version
get_installedversion()

# list number of items in container 
containernumber = xbmc.getInfoLabel('Container.NumItems')


 
    
printstar()
printscript()
print ("Current window is %s" % name)
print ("Current control is %s" % control)
print ("Current window id is %s" % win)
print ("window is %s" % window)
print ("Focus is %s" % focus)
print ("Favourites window is %s visible" % fav)
print ('Container.FolderPath is %s'% FolderPath)
print ('Container.FolderName is %s'% FolderName)
print ("pvr is %s loading"% pvrloading)
print ('CurrentWindowDialogID is %s'% dialog)
# print ('version_installed is %s'% version_installed)
print ('json_query is %s'% json_query)
print ('version is %s'% version)

num = len(running)
if num == 0:
    print 'no addons running'
else:
    print 'addons running are:'
    c = 0
    while c < num:
        e = c + 1
        next = running[c]
        print ('%d.  %s'% (e, next))
        c = c + 1
        
print ('containernumber = %s'% containernumber) 
u = int(containernumber)
print ('u = %d'% u)
if u > 2:
    c = 2
    cont = []
    print 'Container contents are:'
    while c < u:
        # next = xbmc.getInfoLabel('Container.ListItem(%d).Label'% c)
        # Container(id).ListItemAbsolute(id).[infolabel]
        # next = xbmc.getInfoLabel('Container.ListItemAbsolute(%d).[infolabel]'% c)
        next = xbmc.getInfoLabel('Container.ListItemAbsolute(%d).Label'% c)
        cont.append(next)
        print next
        c = c + 1
        

    
printstar()
xbmc.executebuiltin('Notification(Check log, for results)')
exit()