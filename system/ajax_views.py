
from jsonrpcserver import jsonrpc_function
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import sys
import ajax
import runpy

def shellserver(command):
    saved_argv = sys.argv
    # patch sys.argv[1:] and load new command line parameters
    # run_path() does change only sys.argv[0] but restores it
    runpy.run_path('/ecoude_cooking/shellserver/daemondispatcher.py '+command, run_name="__main__")
    sys.argv = saved_argv # restore sys.argv

@login_required
@jsonrpc_function
def loadLoginWindow(request):
    return "alert('login required');"

@jsonrpc_function
def plus(request,a,b):
    return a+b

@jsonrpc_function
def admin_shellserver_refresh(request):
    if (request.user.username == "admin"):
        return ajax.htmlEncode(render_to_string('ajax/admin_shellserver_refresh.html', ajax.admin_shellserver_refresh()))

@jsonrpc_function
def admin_shellserver_start(request,port):
    if (request.user.username == "admin"):
        run('start '+port)
        return ajax.htmlEncode(render_to_string('ajax/admin_shellserver_refresh.html', ajax.admin_shellserver_refresh()))

@jsonrpc_function
def admin_shellserver_stop(request,port):
    if (request.user.username == "admin"):
        run('stop '+port)
        return ajax.htmlEncode(render_to_string('ajax/admin_shellserver_refresh.html', ajax.admin_shellserver_refresh()))

@jsonrpc_function
def admin_shellserver_restart(request,port):
    if (request.user.username == "admin"):
        run('restart '+port)
        return ajax.htmlEncode(render_to_string('ajax/admin_shellserver_refresh.html', ajax.admin_shellserver_refresh()))