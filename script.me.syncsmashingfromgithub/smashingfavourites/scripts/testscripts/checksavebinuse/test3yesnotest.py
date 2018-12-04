# yesnotest
  
import xbmcgui
import xbmc

yesnowindow = xbmcgui.Dialog().yesno("Just testing yesno","Click yes to get a well done","Click No to get a raspberry")

def YES():
    xbmc.executebuiltin('Notification(You have earned, a well done)')

def NOOPTION():
    xbmc.executebuiltin('Notification(You have earned, a raspberry)')
	
def test():
    xbmc.executebuiltin('Notification(You have earned, a poop)')

if yesnowindow:
    YES()

else:
    NOOPTION()
	