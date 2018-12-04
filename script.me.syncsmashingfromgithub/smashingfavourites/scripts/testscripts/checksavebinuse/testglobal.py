# -*- coding: utf-8 -*-
# test Global
import xbmc


#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

test = 1

def testy():
    global test
    test = test + 1
	
def testy2():
    global test
    test = test + 1
	
printstar()
print ('test = %d' % test)
testy()
print ('test = %d' % test)
testy2()
print ('test = %d' % test)
printstar()