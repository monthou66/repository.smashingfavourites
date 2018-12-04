# -*- coding: utf-8 -*-


activeskin = xbmc.translatePath('special://skin')
activeskin = activeskin[:-1]                    # removes backslash to match against skinfolder to check if need to reload skin








# Get os
def getos():
    global PLATFORM, logmessage, logmessage2, error, host
    host = socket.gethostname()
    if xbmc.getCondVisibility('system.platform.android'):
        PLATFORM = 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        PLATFORM = 'linux'
        if xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
            PLATFORM = 'libreelec'
        else:
            error = 'Platform identifies as linux but not as libreelec.'
            errormessage()
            
    elif xbmc.getCondVisibility('system.platform.windows'):
        PLATFORM = 'windows'
    else:
        error = 'Unable to identify the system platform.'
        errormessage()
    # log results:
    logmessage = ('Hostname is %s' % host)
    logmessage2 = ('You\'re using %s' % PLATFORM)
    printlog()
    
# get IP
def getIP
global ip
print 'running getIP()'
ip = xbmc.getIPAddress()

# get current skin
skindir = xbmc.getSkinDir()
