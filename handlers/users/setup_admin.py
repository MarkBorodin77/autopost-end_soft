from aiogram import types
from aiogram.dispatcher import FSMContext

import data.config
from keyboards.inline import setup_admin_keyboard, return_menu_keyboard
from loader import dp, bot
from states import AdminSetupState


@dp.callback_query_handler(lambda c: c.data == "setup_admin")
async def _(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text('<b>⚖ Админы</b>\n\n➕ — Добавить админа\n➖ — Убрать админа', reply_markup=setup_admin_keyboard)

@dp.callback_query_handler(lambda c: c.data == "add_admin")
async def _(query: types.CallbackQuery, state: FSMContext):
    await AdminSetupState.ADD_ADMIN.set()
    await query.message.edit_text('<b>⚖ Админы</b>\n\nСкинь ID аккаунта которому хочешь предоставить доступ к боту.', reply_markup=return_menu_keyboard)
    await state.update_data(message_id=query.message.message_id)

@dp.message_handler(state=AdminSetupState.ADD_ADMIN)
async def _(msg: types.Message, state: FSMContext):
    add_id = msg.text

    state_data = await state.get_data()

    edited_message_id = state_data["message_id"]

    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await bot.edit_message_text(text=f'<b>⚖ Админы</b>\n\nАккаунту с ID {add_id} был <b>успешно</b> предоставлен доступ к боту.', chat_id=msg.from_user.id, message_id=edited_message_id, reply_markup=return_menu_keyboard)


    data.config.ADMINS.append(add_id)

@dp.callback_query_handler(lambda c: c.data == "delete_admin")
async def _(query: types.CallbackQuery, state: FSMContext):
    await AdminSetupState.DELETE_ADMIN.set()
    await query.message.edit_text('<b>⚖ Админы</b>\n\nСкинь ID аккаунта у которого хочешь забрать доступ к боту.', reply_markup=return_menu_keyboard)
    await state.update_data(message_id=query.message.message_id)

@dp.message_handler(state=AdminSetupState.DELETE_ADMIN)
async def _(msg: types.Message, state: FSMContext):
    delete_id = msg.text

    state_data = await state.get_data()

    edited_message_id = state_data["message_id"]

    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await bot.edit_message_text(text=f'<b>⚖ Админы</b>\n\nУ аккаунта с ID {delete_id} был <b>успешно</b> забран доступ к боту.', chat_id=msg.from_user.id, message_id=edited_message_id, reply_markup=return_menu_keyboard)

    data.config.ADMINS.remove(delete_id)

