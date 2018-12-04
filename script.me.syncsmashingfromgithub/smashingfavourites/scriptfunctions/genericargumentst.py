# -*- coding: utf-8 -*-

def getarguments():
    global arguments, choice
    print 'running getarguments()'
    arguments = []
    size = len(sys.argv)
    print ('size is %s'% size)
    if len(sys.argv) > 1:
        choice = 'true'
        c = 1
        num = len(sys.argv)
        num = num + 1
        while c < num:
            d = sys.argv[c]
            arguments.append(d)
            c = c + 1


def getoptions():
    global error, error2, addon, data, backup, nobackup
    print 'running getoptions()'
    size = len(sys.argv)
    print ('size is %s'% size)
    if len(sys.argv) > 1:
        c = 1
        num = len(sys.argv)
        while c < num:
            d = sys.argv[c]
            if d[:5] == 'addon':
                addon = d[8:]           # ie argument is 'addon = xyz', addon (script variable) is 'xyz'
                print ('addon is %s'% addon)
            elif d[:4] == 'data':
                data = d[7:]
                print ('data is %s'% data)
            elif d == 'backup':
                backup = 'true'
                nobackup = 'false'
            elif d == 'nobackup':
                nobackup = 'true'
                backup = 'false'
            elif d == 'force':
                force = 'true'
            elif d == 'previousdata':
                previousdata = 'true'
                data = 'previous'
            elif d == 'default':
                default = 'true'
            else:
                error = 'Invalid argument'
                error2 = ('Argument (%s) not recognised'% d)
                errormessage()
            c = c + 1          