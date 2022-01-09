import psutil
from collections import namedtuple
from datetime import datetime
from functools import wraps
import logging.config

from config.settings import LOGGING

SystemInfo = namedtuple(
    'SystemInfo',
    ['cpu_count', 'cpu_percent', 'cpu_virtual_memory', 'disk_usage', 'boot_time', 'users']
)

AVAILABLE_MEMORY_THRESHOLD = 100 * 1024 * 1024  # 100 Мб
DISK_AVAILABLE_THRESHOLD = 3 * 1024 ** 3        # 3 Гб
CPU_PERCENT_THRESHOLD = 80

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


@write_log_errors
def start():
    info = SystemInfo(
        cpu_count=calc_cpu_count(),
        cpu_percent=calc_cpu_percent(),
        cpu_virtual_memory=calc_virtual_memory(),
        disk_usage=calc_disk_usage(),
        boot_time=calc_boot_time(),
        users=get_users(),
    )
    report_message = '\n\n'.join(info)
    write_log_report(report_message)
    return report_message


def calc_cpu_count():
    logical = f'`{"Логические":13}: {psutil.cpu_count(logical=True)}`'
    physical = f'`{"Физические":13}: {psutil.cpu_count(logical=False)}`'
    return f'*Кол-во ядер процессора*\n{physical}\n{logical}'


def calc_cpu_percent():
    cpu_percent_total = psutil.cpu_percent(interval=0.1, percpu=True)
    if not cpu_percent_total:
        return 'Нет данных'
    warning = ' ❗' if sum(cpu_percent_total) / len(cpu_percent_total) > CPU_PERCENT_THRESHOLD else ''
    data = [f'`{value:.1f}%`' for value in cpu_percent_total]
    return f'*Загрузка ядер*\n{" | ".join(data)}{warning}'


def calc_virtual_memory():
    mem_data = psutil.virtual_memory()
    total, used, available = mem_data.total, mem_data.used, mem_data.available
    warning = ' ❗' if available < AVAILABLE_MEMORY_THRESHOLD else ''
    return f'*Использование памяти*\n`{"Всего":13}: {bytes2human(total)}`' \
           f'\n`{"Использовано":13}: {bytes2human(used)}`' \
           f'\n`{"Доступно":13}: {bytes2human(available)}`{warning}'


def calc_disk_usage():
    paths = [disk.device for disk in psutil.disk_partitions()]
    data_list = []
    for path in paths:
        try:
            data_list.append(psutil.disk_usage(path))
        except PermissionError:
            del path
    stats = '\n\n'.join([f'{path}\n`{"Всего":13}: {bytes2human(data.total)}`\n'
                         f'`{"Использовано":13}: {bytes2human(data.used)}`\n'
                         f'`{"Доступно":13}: {bytes2human(data.free)}`' for path, data in zip(paths, data_list)])
    return f'*Использование дискового пространства*\n{stats}'


def calc_boot_time():
    return f'*Время загрузки системы*\n`{datetime.fromtimestamp(psutil.boot_time()):%d.%m.%Y %H:%M:%S}`'


def get_users():
    users = '\n'.join([f'Имя: {user.name} | Хост: {user.host} | '
                       f'Создан: {datetime.fromtimestamp(user.started):%d.%m.%Y %H:%M:%S}' for user in psutil.users()])
    return f'*Пользователи*\n`{users}`'
