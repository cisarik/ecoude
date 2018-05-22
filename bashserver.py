import os
import sys
import socket
import resource
import subprocess

## Set maximum CPU time to 1 second in child process, after fork() but before exec()
def setlimits():
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))

acceptor = socket.socket()
acceptor.bind(('0.0.0.0', 9000))
acceptor.listen(10)

for i in range(30):
    pid = os.fork()
    if pid == 0:
        childpid = os.getpid()
        try:
            while 1:
                conn, addr = acceptor.accept()
                flo = conn.makefile()
                flo.write('HELLO\n')
                flo.flush()
                if (flo.readline()!='HELLO'):
                    conn.close()
                priority=flo.readline()[9:]
                flo.write('START\n')
                flo.flush()
                os.system("renice -n %s %s" % (priority, childpid))
                subprocess.call([r'/bin/bash'],stdin=flo,stdout=flo,preexec_fn=setlimits);
                flo.write('DONE\n')
                flo.flush()
                if (flo.readline()=='CLOSE'):
                    conn.close()   
        except socket.error, e:
   		print "A socket error"
	except IOError, e:
    		if e.errno == errno.EPIPE:
        		print "EPIPE error"
    		else:
        		print "Other error"
	except KeyboardInterrupt:
		sys.exit()

os.waitpid(-1, 0)

# Sit back and wait for all child processes to exit.
#
# Trap interrupts, write a note, and exit immediately in
# parent. This trap is not inherited by the forks because it
# runs after forking has commenced.
#try:
#    os.waitpid(-1, 0)
#except KeyboardInterrupt:
#    print "\nKeyboardInterrupt"
#    sys.exit()
