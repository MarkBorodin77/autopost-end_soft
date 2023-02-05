from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import return_menu_btn

start_working_spam = InlineKeyboardButton("🟢 Во включенные чаты", callback_data="start_working_spam")
start_all_spam = InlineKeyboardButton("🔥 Во все чаты", callback_data="start_all_spam")
stop_all_spam = InlineKeyboardButton("🚫 Остановить спам", callback_data="stop_all_spam")

control_spam_keyboard = InlineKeyboardMarkup(row_width=2).row(start_working_spam, start_all_spam).add(stop_all_spam).add(return_menu_btn)