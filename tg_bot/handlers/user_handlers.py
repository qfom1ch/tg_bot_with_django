from telebot import TeleBot, types
from telebot.types import Message

from tg_bot.keboards.users_keyboards import markup_change_or_end
from tg_bot.lexicon import LEXICON
from tg_bot.services import UserService

User_dct = {}


def start_registration(message: Message, bot: TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Принять')
    markup.add(item)
    bot.send_message(message.chat.id, LEXICON['/registration'], reply_markup=markup)


def registration_stage_1(message: Message, bot: TeleBot):
    msg = bot.send_message(message.from_user.id, 'Введите номер телефона без +7: ',
                           reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, registration_stage_2, bot=bot)


def registration_stage_2(message: Message, bot: TeleBot):
    if message.text.isdigit() and len(message.text) == 10:
        if UserService.check_user_is_registered('+7' + message.text):
            bot.send_message(message.chat.id, 'Вы зарегистрированы.')
        else:
            User_dct['phone'] = '+7' + message.text
            User_dct['tg_user_id'] = message.from_user.id
            msg = bot.send_message(message.from_user.id, 'Введите имя: ')
            bot.register_next_step_handler(msg, registration_stage_3, bot=bot)
    else:
        msg = bot.send_message(message.from_user.id,
                               'Номер телефона введен некорректно, (номер состоит из 10 цифр) '
                               'попробуйте еще раз (без +7): ')
        bot.register_next_step_handler(msg, registration_stage_2, bot=bot)


def registration_stage_3(message: Message, bot: TeleBot):
    if message.text.isalpha() and 2 < len(message.text) < 15:
        User_dct['first_name'] = message.text
        msg = bot.send_message(message.from_user.id, 'Введите фамилию: ')
        bot.register_next_step_handler(msg, registration_stage_4, bot=bot)
    else:
        msg = bot.send_message(message.from_user.id,
                               'Имя введено некорректно, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, registration_stage_3, bot=bot)


def registration_stage_4(message: Message, bot: TeleBot):
    if message.text.isalpha() and 2 < len(message.text) < 15:
        User_dct['last_name'] = message.text
        bot.send_message(message.from_user.id, f'Ваша учетная запись:\n'
                                               f'Имя - "{User_dct["first_name"]}"\n'
                                               f'Фамилия - "{User_dct["last_name"]}"',
                         reply_markup=markup_change_or_end)
    else:
        msg = bot.send_message(message.from_user.id,
                               'Фамилия введена некорректно, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, registration_stage_4, bot=bot)


def change_first_name_stage_1(message: Message, bot: TeleBot):
    msg = bot.send_message(message.from_user.id, 'Введите новое имя: ', reply_markup=types.ReplyKeyboardRemove())
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
    msg = bot.send_message(message.from_user.id, 'Введите новую фамилию: ', reply_markup=types.ReplyKeyboardRemove())
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
        bot.send_message(message.chat.id, 'Регистрация завершена.', reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Регистрация не удалась, попробуйте еще раз /start.',
                         reply_markup=types.ReplyKeyboardRemove())
