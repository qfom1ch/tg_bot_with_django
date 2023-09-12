from telebot import TeleBot, types
from telebot.types import Message

from tg_bot.keyboards.users_keyboards import markup_change_or_end
from tg_bot.lexicon import LEXICON
from tg_bot.services import UserService

User_dct = {}


def start_registration(message: Message, bot: TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton(text="Принять", request_contact=True)
    markup.add(item)
    bot.send_message(message.chat.id, LEXICON['/registration'],
                     reply_markup=markup)


def registration_stage_1(message: Message, bot: TeleBot):
    if UserService.check_user_is_registered(message.contact.phone_number):
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы.',
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Учетная запись создана.',
                         reply_markup=types.ReplyKeyboardRemove())
        User_dct['phone'] = message.contact.phone_number
        User_dct['tg_user_id'] = message.from_user.id
        User_dct['first_name'] = message.from_user.username
        User_dct['last_name'] = message.from_user.last_name
        bot.send_message(message.chat.id, 'Ваша учетная запись:\n'
                                          f'Имя - "{User_dct["first_name"]}"\n'
                                          f'Фамилия - "{User_dct["last_name"]}"',
                         reply_markup=markup_change_or_end)


def change_first_name_stage_1(message: Message, bot: TeleBot):
    msg = bot.send_message(message.from_user.id, 'Введите новое имя: ',
                           reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, change_first_name_stage_2, bot=bot)


def change_first_name_stage_2(message: Message, bot: TeleBot):
    if message.text.isalpha() and 2 < len(message.text) < 15:
        User_dct['first_name'] = message.text
        bot.send_message(message.from_user.id, f'Ваша учетная запись:\n'
                                               f'Имя - "{User_dct["first_name"]}"\n'
                                               f'Фамилия - "{User_dct["last_name"]}"',
                         reply_markup=markup_change_or_end)
    else:
        msg = bot.send_message(message.from_user.id,
                               'Имя введено некорректно, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, change_first_name_stage_2, bot=bot)


def change_last_name_stage_1(message: Message, bot: TeleBot):
    msg = bot.send_message(message.from_user.id, 'Введите новую фамилию: ',
                           reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, change_last_name_stage_2, bot=bot)


def change_last_name_stage_2(message: Message, bot: TeleBot):
    if message.text.isalpha() and 2 < len(message.text) < 15:
        User_dct['last_name'] = message.text
        bot.send_message(message.from_user.id, f'Ваша учетная запись:\n'
                                               f'Имя - "{User_dct["first_name"]}"\n'
                                               f'Фамилия - "{User_dct["last_name"]}"',
                         reply_markup=markup_change_or_end)
    else:
        msg = bot.send_message(message.from_user.id,
                               'Фамилия введена некорректно, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, change_last_name_stage_2, bot=bot)


def end_registration(message: Message, bot: TeleBot):
    try:
        UserService.user_create(**User_dct)
        bot.send_message(message.chat.id, 'Регистрация завершена.',
                         reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id,
                         'Регистрация не удалась, попробуйте еще раз /start.',
                         reply_markup=types.ReplyKeyboardRemove())
