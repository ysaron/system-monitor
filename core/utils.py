from functools import wraps
from collections import namedtuple
import logging.config

from config.settings import LOGGING


SystemInfo = namedtuple(
    'SystemInfo',
    ['cpu_count', 'cpu_percent', 'cpu_virtual_memory', 'disk_usage', 'boot_time']
)

logging.config.dictConfig(LOGGING)
logger_report = logging.getLogger('report_logger')
logger_errors = logging.getLogger('error_logger')


def bytes2human(num: int, suffix="байт"):

    if not isinstance(num, int):
        return num

    # единицы измерения приняты в соответствии с ГОСТ 8.417
    for unit in ["", "К", "М", "Г", "Т", "П"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Э{suffix}"


def write_log_report(message: str):
    report_message = message.replace('`', '').replace('*', '____')
    logger_report.info(msg=report_message)


def write_log_errors(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger_errors.error(f'{e.__class__.__name__}: {e}')
            raise e

    return wrapper
