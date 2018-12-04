#!/usr/bin/python

print "testing********************************************************************************"
mess = sys.argv[1]

def message():
    if mess == 1:
	    message = "one"
    elif mess == 2:
	    message = "two"
    else:
        message = "balls"

print message()    
print "testing********************************************************************************"
exit()