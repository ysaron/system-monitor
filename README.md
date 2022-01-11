# system-monitor  
Приложение для мониторинга VPS.  

## Описание

- Настраиваемое время измерений.
- Запись отчета в логи.
- Ежедневная отправка отчета в Telegram и отправка отчета по команде.
- Поддерживаемые ОС: Linux, Windows.

На текущий момент измеряются:

- загруженность процессора;
- использование RAM;
- использование дискового пространства;
- время последней загрузки системы.


## Установка (Linux)
### Требования

- Python 3.10
- python3.10-venv

### Установка

Клонировать репозиторий
```shell
git clone https://github.com/ysaron/system-monitor.git
cd system-monitor
```

Создать и активировать виртуальное окружение
```shell
python3.10 -m venv venv
source venv/bin/activate
```

Установить зависимости
```shell
pip3 install -r requirements.txt
```

Получить токен бота Telegram у [@BotFather](https://t.me/BotFather).  
В каталоге `/config/` создать файл `.env` и задать в нем следующие переменные:
```shell
TOKEN="токен бота, полученный от BotFather"
MY_ID=ваш Telegram ID
```
Запуск
```shell
python3.10 bot.py
```
Команда `/start` бота должна генерировать отчет.

### Создание службы автоматического перезапуска

```shell
cd /etc/systemd/system
```
Создать файл `monitorbot.service` следующего содержания (комментарии убрать):
```shell
[Unit]
Description=SOME DESCRIPTION    # произвольное описание
After=network.target

[Service]
Type=simple
User=USER     # пользователь, под которым запускать службу
WorkingDirectory=DIRECTORY   # абсолютный путь к каталогу system-monitor
ExecStart=/.../system-monitor/venv/bin/python3.10 bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Запуск службы
```shell
systemctl daemon-reload
systemctl enable monitorbot.service
systemctl start monitorbot
```
Управление службой
```shell
systemctl status monitorbot
systemctl stop monitorbot
systemctl restart monitorbot
```

### Конфигурация

Расписание измерений задается в `/config/config.yaml`.
