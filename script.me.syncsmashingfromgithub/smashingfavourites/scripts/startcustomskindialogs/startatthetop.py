# -*- coding: utf-8 -*-

import xbmc


	

choice = sys.argv[1]

xbmc.executebuiltin( "ActivateWindow(%s,return)"% choice )
xbmc.executebuiltin( "XBMC.Action(FirstPage)" )