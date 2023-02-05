from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import return_menu_btn

add_admin = InlineKeyboardButton("➕", callback_data="add_admin")
delete_admin = InlineKeyboardButton("➖", callback_data="delete_admin")

setup_admin_keyboard = InlineKeyboardMarkup(row_width=2).row(add_admin, delete_admin).add(return_menu_btn)

