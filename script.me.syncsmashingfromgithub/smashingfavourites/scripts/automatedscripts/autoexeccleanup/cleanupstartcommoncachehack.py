# -*- coding: utf-8 -*-
import xbmc
import os

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")	
AUTOEXEC = os.path.join(USERDATA, "autoexec.py")
tempex = 'commoncachehackautoexec.py'
TEMPEXEC = os.path.join(SMASHINGFAVOURITES, "scripts", "automatedscripts", "autoexec", tempex)
EXTRATEMPAUTOEXEC = os.path.join(USERDATA, "extratempautoexec.py")
RESTOREAUTOEXEC = os.path.join(USERDATA, "restoreoriginalautoexec.py")
DATAFOLDER = xbmc.translatePath('special://home')
ADDONSFOLDER = os.path.join(DATAFOLDER, "addons")
COMMONCACHE = os.path.join(ADDONSFOLDER, "script.common.plugin.cache")
DATATEMP = os.path.join(SMASHINGFAVOURITES, "tempfiles")			
TEMPCOMMONCACHE = os.path.join(DATATEMP, "tempscript.common.plugin.cache")			
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "enableaddonspydone.txt")

# cleanup
if os.path.exists(MARKER):
    os.remove(MARKER)
	
# hackyhack commoncachebollocks
if os.path.exists(TEMPCOMMONCACHE):
    if not os.path.exists(COMMONCACHE):
        os.rename(TEMPCOMMONCACHE, COMMONCACHE)
    else:
        os.remove(TEMPCOMMONCACHE)

###################################################################################
# extra
xbmc.executebuiltin('UpdateLocalAddons')
xbmc.sleep(300)
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "script.common.plugin.cache","enabled":true}}')
xbmc.sleep(300)
if not xbmc.getCondVisibility('System.HasAddon(script.common.plugin.cache)'):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "script.common.plugin.cache","enabled":true}}')

####################################################################################
# and check the rest		

xbmc.executebuiltin('RunScript(special://masterprofile/smashing/smashingfavourites/scripts/automatedscripts/enableaddons.py)')		

###################################################

# wait for enableaddons.py to do its thang				
c = 0
while c < 10:
    xbmc.sleep(1000)
    if os.path.exists(MARKER):
        xbmc.sleep(1000)
        os.remove(MARKER)
        c = 10
    else:
        c = c + 1
####################################################
# cleanup
if os.path.exists(AUTOEXEC):
    liness = file(AUTOEXEC, 'r').readlines()
    lastlines = liness[-1].strip()
    firstfiveletters = lastlines[:5]
    if firstfiveletters == '#temp':
        if not lastlines == ('#temp %s' % tempex):
                xbmcgui.Dialog().ok('Check autoexec.py.', 'There was a problem running cleanupstartcommoncachehack.py')
                exit()
        else:
            os.remove(AUTOEXEC)

if os.path.exists(EXTRATEMPAUTOEXEC):				
    xbmc.executebuiltin('RunScript(special://masterprofile/extratempautoexec.py)')
    # and wait a bit
    xbmc.sleep(5000)
    os.remove(EXTRATEMPAUTOEXEC)
	
if os.path.exists(RESTOREAUTOEXEC):
    if os.path.exists(AUTOEXEC):
        xbmcgui.Dialog().ok('Check autoexec.py.', 'There was a problem running cleanupstartcommoncachehack.py')
    else:
        os.rename(RESTOREAUTOEXEC, AUTOEXEC)
        xbmc.executebuiltin('RunScript(special://masterprofile/autoexec.py)')
		
print 'cleanupstartcommoncachehack.py is DONE!'
exit()

# More beer