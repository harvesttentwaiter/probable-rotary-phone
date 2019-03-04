def pairSpawn(fn, dat):
    signal.signal(signal.SIGCHLD, pairSpawnSigC)
    while True:
        pid = os.fork()

        if pid==0:
            # child
            while True:
                fn(dat)
                pairSpawnChildCheck(fn, dat)

        # parent
        while True:
            # check for child pid
            try:
                os.kill(pid,0)
            except OSError:
                break
            time.sleep(17)

def pairSpawnSigC(signum, frame):
    os.wait()

def pairSpawnChildCheck(fn, dat):
    ppid = os.getppid()
    if ppid == 1:
        pairSpawn(fn, dat)


def createDaemon():
   try:
      pid = os.fork()
   except OSError, e:
      raise Exception, "%s [%d]" % (e.strerror, e.errno)

   if (pid == 0):   # The first child.
      os.setsid()
      try:
         pid = os.fork()    # Fork a second child.
      except OSError, e:
         raise Exception, "%s [%d]" % (e.strerror, e.errno)

      if (pid == 0):    # The second child.
         os.chdir(WORKDIR)
         os.umask(UMASK)
      else:
         os._exit(0)    # Exit parent (the first child) of the second child.
   else:
      os._exit(0)   # Exit parent of the first child.


   maxfd = MAXFD
   for fd in range(0, maxfd):
      try:
         os.close(fd)
      except OSError:   # ERROR, fd wasn't open to begin with (ignored)
         pass

   os.open(REDIRECT_TO, os.O_RDWR)  # standard input (0)

   # Duplicate standard input to standard output and standard error.
   os.dup2(0, 1)            # standard output (1)
   os.dup2(0, 2)            # standard error (2)

   return(0)
