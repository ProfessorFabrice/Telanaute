#!/usr/bin/python
# -*- coding: utf-8

##
# projet Telanaute
# LLI 2004
# Classe Deamon
##


import os
import signal
import sys
import time

##
# cette classe sera utilisee pour la creation d'un deamon
# @param pidfile nom complet (chemin+nom) du fichier contenant le pid du processus
# @param usage_param chaine contenant les parametres a afficher dans l'usage
# @param action chaine contenant l'action a effectue (start, stop, stop-force, restart)

class Deamon:

    def __init__(self,pidfile,usage_param,action):
        self.pidfile=pidfile
        self.startmsg='started with pid %s'
        self.usage_param=usage_param
        self.action=action
        
    
    ##
    # methode permettant de creer un daemon    
    def __deamonize(self,stdout='/dev/null', stderr=None, stdin='/dev/null'):
        '''
            This forks the current process into a daemon.
            The stdin, stdout, and stderr arguments are file names that
            will be opened and be used to replace the standard file descriptors
            in sys.stdin, sys.stdout, and sys.stderr.
            These arguments are optional and default to /dev/null.
            Note that stderr is opened unbuffered, so
            if it shares a file with stdout then interleaved output
            may not appear in the order that you expect.
        '''
        # Do first fork.
        try: 
            pid = os.fork() 
            if pid > 0: sys.exit(0) # Exit first parent.
        except OSError, e: 
            sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)
            
        # Decouple from parent environment.
        os.chdir(self.option.getRacine()) 
        os.umask(0) 
        os.setsid() 
        
        # Do second fork.
        try: 
            pid = os.fork() 
            if pid > 0: sys.exit(0) # Exit second parent.
        except OSError, e: 
            sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        # Open file descriptors and print start message
        if not stderr: stderr = stdout
        si = file(stdin, 'r')
        so = file(stdout, 'a+')
        se = file(stderr, 'a+', 0)
        pid = str(os.getpid())
        sys.stderr.write("\n%s\n" % self.startmsg % pid)
        sys.stderr.flush()
        if self.pidfile: file(self.pidfile,'w+').write("%s\n" % pid)
        
        # Redirect standard file descriptors.
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
    ##
    # methode permettant de demarrer et d'arreter le daemon
    def startStop(self,stdout='/dev/null', stderr=None, stdin='/dev/null'):
        if len(sys.argv) > 2:
            try:
                pf  = file(self.pidfile,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None
            if 'stop' == self.action or 'restart' == self.action :
                if not pid:
                    mess = "Could not stop, pid file '%s' missing.\n"
                    sys.stderr.write(mess % self.pidfile)
                    sys.exit(1)
                try:
                    while 1:
                        os.kill(pid,signal.SIGTERM)
                        time.sleep(240)
                except OSError, err:
                   err = str(err)
                   if err.find("No such process") > 0:
                       os.remove(self.pidfile)
                       if 'stop' == self.action:
                           sys.exit(0)
                       self.action = 'start'
                       pid = None
                   else:
                       print str(err)
                       sys.exit(1)
            if 'stop-force' == self.action :
                if not pid:
                    mess = "Could not stop, pid file '%s' missing.\n"
                    sys.stderr.write(mess % self.pidfile)
                    sys.exit(1)
		try:
	                os.kill(pid,signal.SIGKILL)
		except:
			pass
                os.remove(self.pidfile)
                sys.exit(0)
            if 'start' == self.action:
                if pid:
                    mess = "Start aborded since pid file '%s' exists.\n"
                    sys.stderr.write(mess % self.pidfile)
                    sys.exit(1)
                self.__deamonize(stdout,stderr,stdin)
                return
        print "usage: %s "+self.usage_param+" start|stop|restart|stop-force" % sys.argv[0]
        sys.exit(2)
    
