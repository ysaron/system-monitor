import time
import threading
from telebot import TeleBot
import schedule

from config.settings import TOKEN, MY_ID
from core import controller

bot = TeleBot(token=TOKEN, parse_mode='MARKDOWN')


@bot.message_handler(commands=['start'], func=lambda message: message.chat.id == MY_ID)
def report_immediately(message):
    """  """
    info = controller.start()
    bot.send_message(chat_id=MY_ID, text=info)
    print('report_immediately()')


def report_to_telegram():
    info = controller.start()
    bot.send_message(chat_id=MY_ID, text=info)
    print('report_to_telegram()')


def report_silently():
    controller.start()
    print('report_silently()')


def run_bot():
    bot.infinity_polling()


def run_schedule():
    schedule.every().day.at('08:00').do(report_to_telegram)
    schedule.every(4).hours.do(report_silently)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    print('START')
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_schedule)
    t1.start()
    t2.start()
