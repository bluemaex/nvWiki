#!/usr/bin/env python
import os, sys, fcntl, time
from subprocess import Popen, PIPE, STDOUT

nvPath = sys.argv[1]
lockFile = "/tmp/nvwiki.lock";
timeout = 120

lock = open(lockFile, 'w')
try:
    fcntl.lockf(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except:
    lock.close()
    print "can not lock file. pleaze wait ..."
    exit()

if(os.path.exists(nvPath + "/.git") == False):
    print nvPath + " is not a git repository! aborting."
    exit()

pipe = Popen('/usr/local/bin/git status', shell=True, stdout=PIPE, stderr=STDOUT, cwd=nvPath)
if 'working directory clean' in pipe.stdout.read():
    print "no update necessary"
    exit()
else:
    time.sleep(timeout)
    cmd = "/usr/local/bin/git add .; /usr/local/bin/git commit -a -m 'nvWiki autosave'"
    pipe = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, cwd=nvPath)
    output = pipe.stdout.read()

    cmd = "/usr/local/bin/growlnotify 'nvWiki' -m 'Commited changes to nvWiki: " + output + "'"
    pipe = Popen(cmd, shell=True, stdout=PIPE)
    print pipe.stdout.read()

lock.close()
