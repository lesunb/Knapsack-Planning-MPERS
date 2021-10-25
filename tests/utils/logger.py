import sys
import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers={
        'api-logger': {'class': 'logging.handlers.RotatingFileHandler',
                           'formatter': 'verbose',
                           'level': logging.DEBUG,
                           'filename': 'logs/api.log',
                           'maxBytes': 52428800,
                           'backupCount': 7},
       
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    loggers={
        'logger': {
            'handlers': ['logger', 'console'],
            'level': logging.DEBUG

        }
    }
)

dictConfig(logging_config)

logger = logging.getLogger('logger')
