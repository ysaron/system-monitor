from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get('TOKEN')
MY_ID = int(os.environ.get('MY_ID'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'reports': {
            'format': f'>>> %(asctime)s [%(levelname)s] %(name)s: \n%(message)s\n\n{"-" * 120}\n',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
        'errors': {
            'format': f'>>> %(asctime)s [%(levelname)s] %(name)s: \n%(message)s\n\n{"-" * 120}\n',
            'datefmt': '%d.%m.%Y %H:%M:%S',
        },
    },
    'handlers': {
        'reports': {
            'level': 'INFO',
            'formatter': 'reports',
            'class': 'logging.FileHandler',
            'filename': './logs/reports.log',
            'encoding': 'utf-8',
        },
        'errors': {
            'level': 'ERROR',
            'formatter': 'reports',
            'class': 'logging.FileHandler',
            'filename': './logs/errors.log',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'report_logger': {
            'handlers': ['reports'],
            'level': 'INFO',
            'propagate': False,
        },
        'error_logger': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
