from telebot import types

markup_inline_choose_time = types.InlineKeyboardMarkup(row_width=1)
time_1 = types.InlineKeyboardButton(text='10:00', callback_data='time:10:00')
time_2 = types.InlineKeyboardButton(text='12:00', callback_data='time:12:00')
time_3 = types.InlineKeyboardButton(text='14:00', callback_data='time:14:00')
time_4 = types.InlineKeyboardButton(text='16:00', callback_data='time:16:00')
time_5 = types.InlineKeyboardButton(text='18:00', callback_data='time:18:00')
exit = types.InlineKeyboardButton(text='Отмена', callback_data='exit')

markup_inline_choose_time.add(time_1, time_2, time_3, time_4, time_5, exit)
