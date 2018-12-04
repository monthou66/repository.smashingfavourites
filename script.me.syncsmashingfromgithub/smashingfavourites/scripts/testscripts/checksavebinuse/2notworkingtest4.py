# yesnotest
  
import xbmcgui
import xbmc

yesnowindow = xbmcgui.Dialog().yesno("Just testing yesno","Click yes to get a well done","Click No to get a raspberry")
YES = xbmc.executebuiltin('Notification(You have earned, a well done)')
NOOPTION = xbmc.executebuiltin('Notification(You have earned, a raspberry)')
test = xbmc.executebuiltin('Notification(You have earned, a poop)')

if yesnowindow:
    YES

else:
    NOOPTION
	