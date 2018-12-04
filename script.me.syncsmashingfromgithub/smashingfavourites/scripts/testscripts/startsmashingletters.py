# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	

xbmc.executebuiltin( "ActivateWindow(2151,return)" )
xbmc.executebuiltin( "XBMC.Action(FirstPage)" )