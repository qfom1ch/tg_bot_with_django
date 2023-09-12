import os

import django
from telegram_bot_calendar import WMonthTelegramCalendar

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import logging

from telebot import TeleBot

from config.settings import TELEGRAM_TOKEN
from tg_bot.handlers.other_handlers import any_message, start_message
from tg_bot.handlers.services_handlers import (callback_date, callback_time,
                                               choose_service_1,
                                               choose_service_2,
                                               exit_from_services,
                                               start_calendar, start_services,
                                               start_services_callback)
from tg_bot.handlers.user_handlers import (change_first_name_stage_1,
                                           change_last_name_stage_1,
                                           end_registration,
                                           registration_stage_1,
                                           start_registration)

logger = logging.getLogger(__name__)


def run():
    token = TELEGRAM_TOKEN
    bot = TeleBot(token)

    def register_handlers():
        # Start
        bot.register_message_handler(start_message, commands=['start'], pass_bot=True)
        # Users
        bot.register_message_handler(start_registration, commands=['registration'], pass_bot=True)
        bot.register_message_handler(registration_stage_1, content_types=['contact'],
                                     pass_bot=True)
        bot.register_message_handler(change_first_name_stage_1, func=lambda message: message.text == 'Изменить имя',
                                     pass_bot=True)
        bot.register_message_handler(change_last_name_stage_1, func=lambda message: message.text == 'Изменить фамилию',
                                     pass_bot=True)
        bot.register_message_handler(end_registration, func=lambda message: message.text == 'Завершить редактирование',
                                     pass_bot=True)
        # Services
        bot.register_message_handler(start_services, commands=['services'], pass_bot=True)
        bot.register_callback_query_handler(start_services_callback, func=lambda call: call.data == 'confirm',
                                            pass_bot=True)
        bot.register_callback_query_handler(exit_from_services, func=lambda call: call.data == 'exit', pass_bot=True)
        bot.register_callback_query_handler(choose_service_1, func=lambda call: call.data == 'service_1',
                                            pass_bot=True)
        bot.register_callback_query_handler(choose_service_2, func=lambda call: call.data == 'service_2',
                                            pass_bot=True)

        bot.register_callback_query_handler(start_calendar, func=lambda call: call.data[-2] == '.',
                                            pass_bot=True)
        bot.register_callback_query_handler(callback_date, func=WMonthTelegramCalendar.func(), pass_bot=True)

        bot.register_callback_query_handler(callback_time, func=lambda call: call.data.split(':')[0] == 'time',
                                            pass_bot=True)

        # Other
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
