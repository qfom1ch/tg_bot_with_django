from telebot import TeleBot, types
from telebot.types import Message


def any_message(message: Message, bot: TeleBot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('/start')
    markup.add(item)
    bot.send_message(message.chat.id, 'Для регистрации регистрации нажмите на кнопку.', reply_markup=markup)
