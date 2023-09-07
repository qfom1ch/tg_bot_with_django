import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import logging

from telebot import TeleBot

from config.settings import TELEGRAM_TOKEN
from tg_bot.handlers.other_handlers import any_message
from tg_bot.handlers.user_handlers import (change_first_name_stage_1, change_last_name_stage_1,
                                           end_registration, start_message,
                                           start_registration)

logger = logging.getLogger(__name__)


def run():
    token = TELEGRAM_TOKEN
    bot = TeleBot(token)

    def register_handlers():
        bot.register_message_handler(start_message, commands=['start'], pass_bot=True)
        bot.register_message_handler(start_registration, func=lambda message: message.text == 'Принять', pass_bot=True)
        bot.register_message_handler(change_first_name_stage_1, func=lambda message: message.text == 'Изменить имя',
                                     pass_bot=True)
        bot.register_message_handler(change_last_name_stage_1, func=lambda message: message.text == 'Изменить фамилию',
                                     pass_bot=True)
        bot.register_message_handler(end_registration, func=lambda message: message.text == 'Завершить редактирование',
                                     pass_bot=True)
        bot.register_message_handler(any_message, content_types=['text'], pass_bot=True)

    register_handlers()

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    bot.infinity_polling()


if __name__ == "__main__":
    run()
