#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess

def shellcmd(args):
  process = subprocess.Popen(args, stderr=open(os.devnull, 'w'))
  output = process.communicate()[0]

def notify(header, text):
  shellcmd(["kodi-send", "--action", "Notification(%s,%s)" % (header, text)])

def shellnotify(args):
  pidfile = "/var/run/shellpy.pid"

  if os.path.isfile(pidfile):
   notify("Already running!", file(pidfile, 'r').read())
   sys.exit(1)

  file(pidfile, 'w').write(" ".join(args))

  try:
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    notify("Starting...", " ".join(args))
    shellcmd(args)
    notify("Finished", " ".join(args))
  finally:
    os.unlink(pidfile)


shellnotify(sys.argv[1:])

# http://forum.kodi.tv/showthread.php?tid=158373&page=124