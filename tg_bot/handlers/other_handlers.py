from telebot import TeleBot, types
from telebot.types import Message


def start_message(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, 'Привет!\n'
                                      'Для регистрации регистрации используйте команду /registration.\n'
                                      'Для выбора услуг /services.')


def any_message(message: Message, bot: TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('/registration')
    markup.add(item)
    bot.send_message(message.chat.id, 'Для регистрации регистрации используйте команду /registration.',
                     reply_markup=markup)
