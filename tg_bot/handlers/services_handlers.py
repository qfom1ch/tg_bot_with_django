import datetime
from typing import Optional

from telebot import TeleBot, types
from telebot.types import CallbackQuery, Message
from telegram_bot_calendar import LSTEP, WMonthTelegramCalendar

from tg_bot.keboards.services_keyboars import markup_inline_choose_time

Service_user_dct = {}

Services = {'service_1.1': 'Услуга - 1.1',
            'service_1.2': 'Услуга - 1.2',
            'service_2.1': 'Услуга - 2.1',
            'service_2.2': 'Услуга - 2.2'}

Services_price = {'service_1.1': 3000,
                  'service_1.2': 5000,
                  'service_2.1': 2000,
                  'service_2.2': 3500}

Services_time = {'time:10:00': '10:00',
                 'time:12:00': '12:00',
                 'time:14:00': '14:00',
                 'time:16:00': '16:00',
                 'time:18:00': '18:00'}


def start_services(message: Optional[Message | CallbackQuery], bot: TeleBot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text='Услуга - 1', callback_data='service_1')
    item_2 = types.InlineKeyboardButton(text='Услуга - 2', callback_data='service_2')
    item_3 = types.InlineKeyboardButton(text='Отмена', callback_data='exit')
    markup.add(item_1, item_2, item_3)
    bot.send_message(message.chat.id, 'Выберите услугу:', reply_markup=markup)


def start_services_callback(callback: CallbackQuery, bot: TeleBot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text='Услуга - 1', callback_data='service_1')
    item_2 = types.InlineKeyboardButton(text='Услуга - 2', callback_data='service_2')
    item_3 = types.InlineKeyboardButton(text='Отмена', callback_data='exit')
    markup.add(item_1, item_2, item_3)
    bot.answer_callback_query(callback_query_id=callback.id, text='Вы записаны.')
    bot.send_message(callback.message.chat.id, 'Выберите услугу:', reply_markup=markup)


def exit_from_services(callback: CallbackQuery, bot: TeleBot):
    bot.send_message(callback.message.chat.id, 'Вы вышли из выбора услуг.\n'
                                               'Для регистрации ипользуйте /registration\n'
                                               'Для выбора услуг /services.')


def choose_service_1(callback: CallbackQuery, bot: TeleBot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text='Услуга - 1.1', callback_data='service_1.1')
    item_2 = types.InlineKeyboardButton(text='Услуга - 1.2', callback_data='service_1.2')
    item_3 = types.InlineKeyboardButton(text='Отмена', callback_data='exit')
    markup.add(item_1, item_2, item_3)
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=markup)


def choose_service_2(callback: CallbackQuery, bot: TeleBot):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text='Услуга - 2.1', callback_data='service_2.1')
    item_2 = types.InlineKeyboardButton(text='Услуга - 2.2', callback_data='service_2.2')
    item_3 = types.InlineKeyboardButton(text='Отмена', callback_data='exit')
    markup.add(item_1, item_2, item_3)
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=markup)


def start_calendar(callback: CallbackQuery, bot: TeleBot):
    Service_user_dct['service'] = Services[callback.data]
    Service_user_dct['price'] = Services_price[callback.data]

    calendar, step = WMonthTelegramCalendar(locale='ru').build()
    bot.send_message(callback.message.chat.id,
                     f"Выберите дату: {LSTEP[step]}".replace('day', ''),
                     reply_markup=calendar)


def callback_date(callback: CallbackQuery, bot: TeleBot):
    result, key, step = WMonthTelegramCalendar(locale='ru').process(callback.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату: {LSTEP[step]}".replace('day', ''),
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        if result < datetime.date.today():
            bot.send_message(callback.message.chat.id,
                             'Выбранна некорректная дата, попробуйте еще раз.')
        else:
            Service_user_dct['date'] = f'{result}'
            bot.send_message(callback.message.chat.id, 'Выберете время: ', reply_markup=markup_inline_choose_time)


def callback_time(callback: CallbackQuery, bot: TeleBot):
    Service_user_dct['time'] = Services_time[callback.data]

    markup = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton(text='Подтвердить', callback_data='confirm')
    item_2 = types.InlineKeyboardButton(text='Отмена', callback_data='exit')
    markup.add(item_1, item_2)
    bot.send_message(callback.message.chat.id, text=f'Подтвердите запись:\n'
                                                    f'Услуга - {Service_user_dct["service"]}\n'
                                                    f'Дата - {Service_user_dct["date"]}\n'
                                                    f'Время - {Service_user_dct["time"]}\n'
                                                    f'Стоимость: {Service_user_dct["price"]} р', reply_markup=markup)
