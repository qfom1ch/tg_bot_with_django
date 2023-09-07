from telebot import types

markup_change_or_end = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
item1 = types.KeyboardButton('Изменить имя')
item2 = types.KeyboardButton('Изменить фамилию')
item3 = types.KeyboardButton('Завершить редактирование')
markup_change_or_end.add(item1, item2, item3)
