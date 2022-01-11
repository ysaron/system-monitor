from dotenv import load_dotenv
import yaml
import os

load_dotenv()

TOKEN = os.environ.get('TOKEN')
MY_ID = int(os.environ.get('MY_ID'))

with open('config/config.yaml') as f:
    cfg = yaml.safe_load(f)

REPORT_TIME = cfg.get('report_to_telegram_time', '08:00')
REPORT_EVERY = cfg.get('report_silently_every_hours', 4)

mem_threshold = cfg.get('mem_threshold', 100)
disk_threshold = cfg.get('disk_threshold', 3)
cpu_threshold = cfg.get('cpu_threshold', 80)

if any(not isinstance(p, int | float) for p in (mem_threshold, disk_threshold, cpu_threshold)):
    raise ValueError('Ошибка конфигурации')

AVAILABLE_MEMORY_THRESHOLD = mem_threshold * 1024 * 1024
DISK_AVAILABLE_THRESHOLD = disk_threshold * 1024 ** 3
CPU_PERCENT_THRESHOLD = cpu_threshold

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
