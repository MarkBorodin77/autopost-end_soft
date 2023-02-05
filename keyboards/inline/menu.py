from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import return_menu_btn

change_account = InlineKeyboardButton("🎩 Сменить аккаунт", callback_data="change_account_menu")
setup_chat = InlineKeyboardButton("⚙ Настроить чаты", callback_data="setup_chat")
setup_admin = InlineKeyboardButton("⚖ Админы", callback_data="setup_admin")
get_info = InlineKeyboardButton("🏝 Инфо", callback_data="get_info")
control_spam = InlineKeyboardButton("⛔ Контролировать спам", callback_data="control_spam")

edit_time = InlineKeyboardButton("🕙 Изменить время", callback_data="edit_time")
edit_text = InlineKeyboardButton("✍ Изменить текст", callback_data="edit_text")
enable_chats = InlineKeyboardButton("✅ Включить чаты", callback_data="enable_chats")
mute_chats = InlineKeyboardButton("❌ Выключить чаты", callback_data="mute_chats")
return_back_btn = InlineKeyboardButton("◀ Вернуться к настройке", callback_data="return_back")
add_photo_btn = InlineKeyboardButton("➕ Добавить фото", callback_data="add_photo")
delete_photo_btn = InlineKeyboardButton("➖ Убрать фото", callback_data="delete_photo")




select_all_chats_btn = InlineKeyboardButton("Выбрать все чаты", callback_data="select_all_chats")


return_setup_chats_menu = InlineKeyboardMarkup(row_width=1).add(return_back_btn, return_menu_btn)

continue_setup_keyboard = InlineKeyboardMarkup(row_width=2).row(edit_time, edit_text).row(enable_chats, mute_chats).row(add_photo_btn, delete_photo_btn).add(return_menu_btn)

menu_keyboard = InlineKeyboardMarkup(row_width=2).add(change_account).add(setup_chat).row(setup_admin, get_info).add(control_spam)
