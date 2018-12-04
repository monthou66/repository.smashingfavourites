# yesnotest
  
import xbmcgui
import xbmc

yesnowindow = xbmcgui.Dialog().yesno("Just testing yesno","Click yes to get a well done","Click No to get a raspberry")
NOOPTION = xbmc.executebuiltin('Notification(You have earned, a raspberry)')


if yesnowindow:
    xbmc.executebuiltin('Notification(You have earned, a well done)')

else:
    NOOPTION
	