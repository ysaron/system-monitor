import time
import threading
from telebot import TeleBot
import schedule

from config.settings import TOKEN, MY_ID, REPORT_TIME, REPORT_EVERY
from core import controller

bot = TeleBot(token=TOKEN, parse_mode='MARKDOWN')


@bot.message_handler(commands=['start'], func=lambda message: message.chat.id == MY_ID)
def report_immediately(message):
    """ Отправляет отчет в Telegram по команде /start """
    info = controller.report(log=False)
    bot.send_message(chat_id=MY_ID, text=info)


def report_daily():
    """ Ежедневно по расписанию отправляет отчет в Telegram и пишет в логи """
    info = controller.report()
    bot.send_message(chat_id=MY_ID, text=info)


def report_silently():
    """ Пишет отчет в логи по расписанию """
    controller.report()


def run_bot():
    bot.infinity_polling()


def run_schedule():
    schedule.every().day.at(REPORT_TIME).do(report_daily)
    schedule.every(REPORT_EVERY).hours.do(report_silently)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_schedule)
    t1.start()
    t2.start()
