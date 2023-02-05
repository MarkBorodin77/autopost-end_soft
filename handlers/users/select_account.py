import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import return_menu_btn, return_menu_keyboard
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "select_account", state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    accounts_keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = []

    for i in os.listdir("sessions"):
        account_name = i.replace(".session", "")
        admin_id = int(account_name.split("_")[-1])
        account_name = account_name.replace(f"_{admin_id}", "")
        if admin_id == query.from_user.id:
            account_btn = InlineKeyboardButton(f"{account_name.replace(f'_{admin_id}', '')}", callback_data=f"select_account_{account_name}")
            buttons.append(account_btn)

    if len(buttons) != 0:
        accounts_keyboard.add(*buttons)

    accounts_keyboard.add(return_menu_btn)

    await query.message.edit_text("<b>🗣 Выбрать аккаунт</b>\n\nВыбери аккаунт который хочешь настроить.", reply_markup=accounts_keyboard)


@dp.callback_query_handler(Text(startswith="select_account_"), state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    account_name = f"{query.data.replace('select_account_', '')}_{query.from_user.id}"

    await state.update_data(account_name=account_name)

    await query.message.edit_text(f"<b>🗣 Выбрать аккаунт</b>\n\nУспешно <b>выбран</b> аккаунт с названием {account_name}.",
                                  reply_markup=return_menu_keyboard)

@dp.callback_query_handler(lambda c: c.data== "delete_account")
async def _(query: types.CallbackQuery, state: FSMContext):
    accounts_keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = []

    for i in os.listdir("sessions"):
        account_name = i.replace(".session", "")
        admin_id = int(account_name.split("_")[-1])
        account_name = account_name.replace(f"_{admin_id}", "")

        if admin_id == query.from_user.id:
            account_btn = InlineKeyboardButton(f"{account_name}", callback_data=f"delete_account_{account_name}")
            buttons.append(account_btn)

    if len(buttons) != 0:
        accounts_keyboard.add(*buttons)

    accounts_keyboard.add(return_menu_btn)

    await query.message.edit_text(f"<b>🗑 Удалить аккаунт</b>\n\nВыбери аккаунт для удаления.",
                                  reply_markup=accounts_keyboard)

@dp.callback_query_handler(Text(startswith="delete_account_"), state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    account_name = query.data.replace("delete_account_", "")

    if os.path.isfile(f'sessions/{account_name}_{query.from_user.id}.session'):
        os.remove(f'sessions/{account_name}_{query.from_user.id}.session')

    await query.message.edit_text(f"<b>🗑 Удалить аккаунт</b>\n\nАккаунт с названием {account_name} успешно удален.",
                                  reply_markup=return_menu_keyboard)