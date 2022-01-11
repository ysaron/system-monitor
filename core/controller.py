import psutil
from datetime import datetime

from .utils import SystemInfo, write_log_errors, write_log_report, bytes2human
from config.settings import AVAILABLE_MEMORY_THRESHOLD, DISK_AVAILABLE_THRESHOLD, CPU_PERCENT_THRESHOLD


@write_log_errors
def report(log: bool = True):
    info = SystemInfo(
        cpu_count=calc_cpu_count(),
        cpu_percent=calc_cpu_percent(),
        cpu_virtual_memory=calc_virtual_memory(),
        disk_usage=calc_disk_usage(),
        boot_time=calc_boot_time(),
    )
    report_message = '\n\n'.join(info)
    if log:
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
    header = '*Использование дискового пространства*\n'
    match True:
        case psutil.LINUX:
            paths = ['/']
        case psutil.WINDOWS:
            paths = [disk.device for disk in psutil.disk_partitions()]
        case _:
            return f'{header}Неподдерживаемая ОС'
    data_list = []
    warnings = []
    for path in paths:
        try:
            data = psutil.disk_usage(path)
            data_list.append(data)
            warning = ' ❗' if data.free < DISK_AVAILABLE_THRESHOLD else ''
            warnings.append(warning)
        except PermissionError:
            del path
    stats = '\n\n'.join([f'{path}\n`{"Всего":13}: {bytes2human(data.total)}`\n'
                         f'`{"Использовано":13}: {bytes2human(data.used)}`\n'
                         f'`{"Доступно":13}: {bytes2human(data.free)}`{warning}'
                         for path, data, warning in zip(paths, data_list, warnings)])
    return f'{header}{stats}'


def calc_boot_time():
    return f'*Время загрузки системы*\n`{datetime.fromtimestamp(psutil.boot_time()):%d.%m.%Y %H:%M:%S}`'
