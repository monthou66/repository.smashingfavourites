import xbmc
import xbmcaddon
import xbmcgui
 
#addon       = xbmcaddon.Addon()
#addonname   = addon.getAddonInfo('name')

#my bit
skindir = xbmc.getSkinDir()
if skindir == "skin.xonfluence":
    skinchoice = "Good choice"
else:
    skinchoice = "Stoopid arse"
	
skincomment = "You're using %s" %(skindir)	
xbmcgui.Dialog().ok(skinchoice, skincomment)
xbmc.sleep(5000)

# end my bit

keyboard = xbmc.Keyboard("", "Type your name", False)
keyboard.doModal()
if keyboard.isConfirmed() and keyboard.getText() != "":
    line1 = "Hello World!"
    line2 = "Nice to meet you %s" %(keyboard.getText())
    line3 = "Welcome to Kodi!"
    xbmcgui.Dialog().ok("bozo", line1, line2, line3)
#    xbmcgui.Dialog().ok(addonname, line1, line2, line3)

# http://mirrors.xbmc.org/docs/python-docs/stable/xbmc.html