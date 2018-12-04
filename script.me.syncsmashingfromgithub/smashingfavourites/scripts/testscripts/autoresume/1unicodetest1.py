#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
   
test = 'ñ'
print ('test is %s'% test)
    
test2 = 'Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Piña Colada Song).mp3'
print ('test2 is %s'% test2)        
    
list = []
list.append(test)
list.append(test2)
print ('list is %s'% list)

check = list[0]
print ('check is %s'% check)

check1 = list[1]
print ('check1 is %s'% check1)
    
xbmc.executebuiltin('Notification(All, done)')



exit()
# results:

# test is ñ
# test2 is Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Piña Colada Song).mp3
# list is ['\xc3\xb1', 'Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Pi\xc3\xb1a Colada Song).mp3']
# check is ñ
# check1 is Guardians of the Galaxy Awesome Mix Vol.1 - 10 - Rupert Holmes - Escape (The Piña Colada Song).mp3







