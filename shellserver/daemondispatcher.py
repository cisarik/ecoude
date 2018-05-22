#!/usr/bin/env python

"""
File: dispatcher.py
    
    
    
"""

import os
import sys
import time
import atexit
import socket
import logging
import resource
import memcache
import subprocess
import logging.config
from signal import SIGTERM 
from logconfig import dictConfig

WORKINGDIR='/ecoude'
CPULIMITSECONDS=3
HOST='127.0.0.1'
PORT=9000

DAEMON_ALREADY_RUNNING_ERROR=10
KILLING_DAEMON_ERROR=11
NO_SUCH_DAEMON_ERROR=12
SOCKET_SHELLSERVER_ERROR=13
EPIPE_SHELLSERVER_ERROR=14
IO_SHELLSERVER_ERROR=15
DAEMON_FORKING_ERROR=16

OK=0
BAD_COMMAND=1

logging.config.dictConfig(dictConfig())
log = logging.getLogger('shellserverdaemon')
log.setLevel(logging.DEBUG)

class shellserverdaemon():

    def __init__(self, workingdir=WORKINGDIR, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', host=HOST, port=PORT,cpulimitseconds=CPULIMITSECONDS):
        self.workingdir=workingdir
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.host=host
        self.port=str(port)
        self.cpulimitseconds=cpulimitseconds
    
    def delpid(self):
        log.debug('delpid called')
        memcache.Client(['127.0.0.1:11211']).delete(self.port)
	
    
    #Do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" 
    #for more details (ISBN 0201563177) or http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
    def daemonize(self):
	log.debug("Daemonize process..")
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) # exit first parent
        except OSError, e: 
            log.error("Fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(DAEMON_FORKING_ERROR)
        
        # decouple from parent environment :
        os.chdir(self.workingdir) 
        os.setsid() 
        os.umask(0) 
        
        try: 
            pid = os.fork() # do second fork
            if pid > 0:
                sys.exit(0) # exit from second parent
        except OSError, e: 
            log.error("Fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(DAEMON_FORKING_ERROR) 
        
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
        
        atexit.register(self.delpid)# at Exit run function for deleting pid file
        pid = str(os.getpid())
	memcache.Client(['127.0.0.1:11211']).add(self.port, pid)
        log.debug("Process pid:%s daemonized and (port:%s,pid:%s) saved to the memcache." % (pid,self.port,pid))
	
    #Start the daemon
    def start(self):
        log.debug("start()")
        pid=memcache.Client(['127.0.0.1:11211']).get(self.port) # Check for a pidfile to see if the daemon already runs    

        if (pid!=None):
            log.warning("Process pid:%s already exist. Daemon already running?" % pid)
            sys.exit(DAEMON_ALREADY_RUNNING_ERROR)

        self.daemonize()
        self.run()
    
    
    #Stop the daemon
    def stop(self):
        log.debug("stop()")
        pid=memcache.Client(['127.0.0.1:11211']).get(self.port)
            
        if (pid==None):
            log.warning("Process pid %s does not exist. Daemon not running?" % pid)
            return # not an error in a restart
        
        log.debug("Try killing the daemon process pid=%s this.pid=%d "  % (pid,os.getpid()))
        try:
            while 1:
                os.kill(int(pid), SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
        	pid=memcache.Client(['127.0.0.1:11211']).get(self.port)
                if (pid!=None):
			memcache.Client(['127.0.0.1:11211']).delete(self.port)
			log.debug("Process for  port:%s deleted from memcache." % self.port)
            else:
                log.debug(str(err))
                sys.exit(KILLING_DAEMON_ERROR)

	log.debug("Daemon pid:%s killed!" % pid)
    
    
    #Restart the daemon
    
    def restart(self):
        self.stop()
        self.start()
    
    
    def run(self):
        acceptor = socket.socket()
        acceptor.bind((self.host, int(self.port)))
	acceptor.listen(10)
        
        log.debug("Running shellserver loop as daemon on the %s:%s" % (self.host,self.port))
        try:
            while 1:
                conn, addr = acceptor.accept()
                log.debug("Connection from %s accepted" % str(addr))
                flo = conn.makefile()
                flo.write('HELLO\n')
                flo.flush()
                if (flo.readline()!='HELLO'):
                    conn.close()
                priority=flo.readline()[9:]
                flo.write('START\n')
                flo.flush()
            	log.debug("Creating /bin/bash subprocess")
                # Set maximum CPU time to 1 second in child process, after fork() but before exec()
                subprocess.call([r'/bin/bash'],stdin=flo,stdout=flo,preexec_fn=resource.setrlimit(resource.RLIMIT_CPU, (self.cpulimitseconds, self.cpulimitseconds)))
		log.debug("Shell subprocess ended")
                flo.write('DONE\n')
                flo.flush()
                if (flo.readline()=='CLOSE\n'):
                    conn.close()
		    log.debug("Closing connection")
        except socket.error, e:
            log.error("A socket error!")
            sys.exit(SOCKET_SHELLSERVER_ERROR)
        except IOError, e:
            if e.errno == errno.EPIPE:
                log.error("EPIPE error!")
                sys.exit(EPIPE_SHELLSERVER_ERROR)
            else:
                log.error("IOError error!")
                sys.exit(IO_SHELLSERVER_ERROR)


if __name__ == "__main__":
        host=HOST
        port=PORT

        if len(sys.argv) == 2:
            if 'list' == sys.argv[1]:
		print(memcache.Client(['127.0.0.1:11211']).flush_all())

	elif len(sys.argv) == 4:
            host=sys.argv[2]
            port=int(sys.argv[3])
    
    	elif len(sys.argv) == 3:
            	port=int(sys.argv[2])

	else:
		print("usage: %s start|stop|restart [host] [port]" % sys.argv[0])
		sys.exit(BAD_COMMAND)

	dispatcherdaemon = shellserverdaemon(host=host,port=port)

	if 'start' == sys.argv[1]:
		dispatcherdaemon.start()

        elif 'stop' == sys.argv[1]:
                dispatcherdaemon.stop()

        elif 'restart' == sys.argv[1]:
                dispatcherdaemon.restart()

        else:
                print("Unknown command")
                print("usage: %s start|stop|restart [host] [port]" % sys.argv[0])
                sys.exit(BAD_COMMAND)

        sys.exit(OK)
