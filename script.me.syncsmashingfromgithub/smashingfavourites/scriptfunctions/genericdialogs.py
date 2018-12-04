# -*- coding: utf-8 -*-

    # get clone_id
    keyboard = xbmc.Keyboard("", "Enter cloned addon id", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        clone_id = keyboard.getText()
        
        
        
        yesnowindow = xbmcgui.Dialog().yesno('New clone id entered is', clone_id, "", "Click Yes to proceed")
        if not yesnowindow:
            error = 'Script cancelled by user'
            errormessage()        
        

    CHOOSE = xbmcgui.Dialog().select("Options", LIST)
    CHOICE = LIST[CHOOSE]
    if not CHOOSE == -1:
        output = whatever[CHOOSE]
        thingy()
    else:
        error = 'Script cancelled by user'
        errormessage()

xbmc.executebuiltin('Notification(Marker file - was not removed)')
xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
xbmc.executebuiltin('Notification(errornotification)')




multi

    folders = []
    files = []
    options = []
    choices = []
    invalid = 'false'
    folders, files = xbmcvfs.listdir(smashingsource)
    options = folders + files
    options
    question = 'Choose options to copy to local folder:'
    a = 'Cancel operation'
    if a not in options:
        options.append(a)
    choicenumbers = xbmcgui.Dialog().multiselect(question, options)
    if choicenumbers == None:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Action, cancelled)')
        exit()
    elif choicenumbers == []:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Action, cancelled)')
        exit()
    else:
        num = len(choicenumbers)
        if num > 0:
            c = 0
            while c < num:
                nextnumber = choicenumbers[c]
                nextnumber = int(nextnumber)
                next = options[nextnumber]
                choices.append(next)
                c = c + 1
            print ('choices = %s'% choices)       
        if num > 1:
            if a in choices:
                invalid = 'true'
    if invalid == 'true':
        yesnowindow = xbmcgui.Dialog().yesno('Invalid options selected', 'Click yes to try again', 'Click no to cancel script')
        if yesnowindow:
            xbmc.sleep(300)
            choosestufftocopy() 
        else:
            print 'Script cancelled by user'
            exit()
            
# yesno
dialog = xbmcgui.Dialog()
ret = dialog.yesno('Do you want to', 'resume playback?', yeslabel = 'yes please', nolabel = 'no thanks', autoclose = 5000)
xbmc.executebuiltin('Notification(ret is, %s)'% ret)
        