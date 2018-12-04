# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import os

# To show up in log:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def printworking():
    print "Doing stuff."
	

	
def addtofavourites():
# add entry to favourites
# identify xonfluence favourites file - take code from smashingfavourites.py
# read current favourite
    FAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile'), "favourites.xml")
# get line 2
    line = open(FAVOURITESFILE).readlines()[1]
# find xonfluence favourites
    CURRENT = line[line.find("/icons/")+7:line.find(".png")]
    if CURRENT != 'xonfluence':
        NEWFAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/xonfluence/favourites.xml")
        if not os.path.isfile(NEWFAVOURITESFILE):
            exit()
# Move favourites files if necessary - code from smashingfavourites.py
        else:
            OLDFAVOURITES = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/", CURRENT)
            OLDFAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/options/", CURRENT, "favourites.xml")            
            os.rename(FAVOURITESFILE, OLDFAVOURITESFILE)
            os.rename(NEWFAVOURITESFILE, FAVOURITESFILE)		
# add the new favourite
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title":"Restore %s", "type":"script", "path":"special://masterprofile/smashing/smashingfavourites/scripts/skinscripts/smashingxonfluence.py, restore, %s", "thumbnail":""}, "id": 1}' % (OPTION, OPTION))
# clean &quot;
    infile = os.path.join(xbmc.translatePath('special://userdata/favourites.xml'))
    outfile = os.path.join(xbmc.translatePath('special://userdata/1favourites.xml'))
    delete_start = ["RunScript(&quot;"]
    delete_end = ["%s&quot;" % OPTION]
    fin = open(infile)
    fout = open(outfile, "w+")
    for line in fin:
        for word in delete_start:
            line = line.replace(word, "RunScript(")
        for word in delete_end:
            line = line.replace(word, "%s" % OPTION)	
        fout.write(line)
    fin.close()
    fout.close()
    os.remove(infile)
    os.rename(outfile, infile)	

