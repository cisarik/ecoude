def dictConfig():
    return {

    'version': 1,

    'disable_existing_loggers': False,

    'formatters': {

    'standard': {
    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    },                  

    'verbose': {
    'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    },

    'simple': {
    'format': '%(levelname)s %(message)s'
    },

    },


    'filters': {
    },


    'handlers': {

    'null': {
    'level':'DEBUG',
    'class':'logging.NullHandler',
    },

    'console':{
    'level':'DEBUG',
    'class':'logging.StreamHandler',
    'formatter': 'standard'
    },

    'default': {
    'level':'ERROR',
    'class':'logging.handlers.RotatingFileHandler',
    'filename': '/var/log/python.log',
    'mode':'w',
    'maxBytes': 1024*1024*100, # 100 MB
    'backupCount': 5,
    'formatter':'standard'
    },  

    'shellserverdaemonlogfile': {
    'level':'DEBUG',
    'class':'logging.handlers.RotatingFileHandler',
    'filename': '/var/log/daemondispatcher.log',
    'mode':'w',
    'maxBytes': 1024*1024*100, # 100 MB
    'backupCount': 5,
    'formatter':'standard'              
    },

    'shellserverdaemonwarning': {
    'level':'WARNING',
    'class': 'logging.handlers.SMTPHandler',
    'mailhost': 'localhost',
    'fromaddr': 'my_app@domain.tld',
    'toaddrs': 'cisary@me.com',
    'subject': 'Houston, we have a problem.',
    'formatter':'standard'
    }

    },

    'loggers': {

    'shellserverdaemon': {
    'handlers': ['shellserverdaemonlogfile'],
    'level': 'DEBUG',  #Or maybe INFO or DEBUG
    'propagate': True,
    },

    }
}