from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

change_account = InlineKeyboardButton("🗣 Выбрать аккаунт", callback_data="select_account")
add_account = InlineKeyboardButton("👀 Добавить аккаунт", callback_data="add_account")
delete_account = InlineKeyboardButton("🗑 Удалить аккаунт", callback_data="delete_account")

return_menu_btn = InlineKeyboardButton("❌ Вернуться в меню", callback_data="return_menu")
skip_btn = InlineKeyboardButton("🔜 Пропустить", callback_data="skip_action_2fa")

right_action_btn = InlineKeyboardButton("▶", callback_data="right_action")
left_action_btn = InlineKeyboardButton("◀", callback_data="left_action")
continue_setup_btn = InlineKeyboardButton("Продолжить", callback_data="continue_setup")

return_menu_keyboard = InlineKeyboardMarkup().add(return_menu_btn)
skip_keyboard = InlineKeyboardMarkup(row_width=1).add(skip_btn).add(return_menu_btn)

change_account_menu_keyboard = InlineKeyboardMarkup(row_width=2).row(change_account, add_account).add(delete_account).add(return_menu_btn)
