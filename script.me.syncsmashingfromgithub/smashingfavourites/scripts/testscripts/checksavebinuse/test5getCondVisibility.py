# -*- coding: utf-8 -*-

import xbmc

print "***************************************************************************************"

if xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):
    print "dvbviewer is enabled"
else:
    print "dvbviewer is not enabled, oh no."
	
print "***************************************************************************************"	

#enabled = str(state)

# print enabled


# return xbmc.getCondVisibility('System.HasAddon(%s)' % script_name) == 1