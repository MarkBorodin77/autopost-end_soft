import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from keyboards.inline import return_menu_keyboard, skip_keyboard
from loader import dp, bot
from states import AddAccountState


@dp.callback_query_handler(lambda c: c.data == "skip_action_2fa", state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(authorization_password="None")
    await AddAccountState.GET_CODE_ACCOUNT.set()

    await send_telegram_code(state, query.from_user.id)

    await query.message.edit_text(
        f"<b>👀 Добавить аккаунт</b>\n\nНа аккаунт было отправлено сообщение с кодом. Дождись пока оно дойдет и отправь сюда.",
        reply_markup=return_menu_keyboard)


@dp.callback_query_handler(lambda c: c.data == "add_account")
async def _(query: types.CallbackQuery, state: FSMContext):
    message_id = query.message.message_id
    await AddAccountState.GET_NAME_ACCOUNT.set()
    await query.message.edit_text("<b>👀 Добавить аккаунт</b>\n\nВведи как я буду <b>называть аккаунт</b>:",
                                  reply_markup=return_menu_keyboard)
    await state.update_data(message_id=message_id)


@dp.message_handler(state=AddAccountState.GET_NAME_ACCOUNT)
async def _(msg: types.Message, state: FSMContext):
    name = msg.text

    del_message_id = msg.message_id
    state_data = await state.get_data()
    edit_message_id = state_data["message_id"]

    await state.update_data(name=name)
    await AddAccountState.GET_API_ID_ACCOUNT.set()
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f'<b>👀 Добавить аккаунт</b>\n\nВведи api_id и api_hash аккаунта через ":". Получить их можно на сайте https://my.telegram.org/auth?to=app.',
                                message_id=edit_message_id, reply_markup=return_menu_keyboard)

    await bot.delete_message(chat_id=msg.from_user.id, message_id=del_message_id)


@dp.message_handler(state=AddAccountState.GET_API_ID_ACCOUNT)
async def _(msg: types.Message, state: FSMContext):
    del_message_id = msg.message_id
    state_data = await state.get_data()
    edit_message_id = state_data["message_id"]

    api_data = msg.text.split(":")
    api_id = int(api_data[0])
    api_hash = api_data[1]

    await state.update_data(api_id=api_id, api_hash=api_hash)
    await AddAccountState.GET_PHONE_ACCOUNT.set()
    await bot.delete_message(chat_id=msg.from_user.id, message_id=del_message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f"<b>👀 Добавить аккаунт</b>\n\nТеперь введи <b>номер телефона</b> аккаунта.",
                                message_id=edit_message_id, reply_markup=return_menu_keyboard)


@dp.message_handler(state=AddAccountState.GET_PHONE_ACCOUNT)
async def _(msg: types.Message, state: FSMContext):
    del_message_id = msg.message_id
    state_data = await state.get_data()
    edit_message_id = state_data["message_id"]

    phone = msg.text

    await state.update_data(phone=phone)

    await AddAccountState.GET_2FA_ACCOUNT.set()
    await bot.delete_message(chat_id=msg.from_user.id, message_id=del_message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f"<b>👀 Добавить аккаунт</b>\n\nЕсли на аккаунте есть 2FA, то введи пароль. Если же нету - нажми на кнопку 'Пропустить'.",
                                message_id=edit_message_id, reply_markup=skip_keyboard)


async def send_telegram_code(state, admin_id):
    state_data = await state.get_data()

    name = state_data["name"]
    api_id = state_data["api_id"]
    api_hash = state_data["api_hash"]
    phone = state_data["phone"]

    if os.path.isfile(f'./sessions/{name}_{admin_id}.session'): os.remove(f'./sessions/{name}_{admin_id}.session')

    client = TelegramClient(f"sessions/{name}_{admin_id}", api_id, api_hash)

    await client.connect()
    phone_hash = await client.send_code_request(phone)
    phone_code_hash = phone_hash.phone_code_hash

    await state.update_data(phone_code_hash=phone_code_hash)


@dp.message_handler(state=AddAccountState.GET_2FA_ACCOUNT)
async def _(msg: types.Message, state: FSMContext):
    authorization_password = msg.text

    del_message_id = msg.message_id
    state_data = await state.get_data()
    edit_message_id = state_data["message_id"]

    await state.update_data(authorization_password=authorization_password)

    await send_telegram_code(state, msg.from_user.id)

    await AddAccountState.GET_CODE_ACCOUNT.set()

    await bot.delete_message(chat_id=msg.from_user.id, message_id=del_message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f"<b>👀 Добавить аккаунт</b>\n\nНа аккаунт было отправлено сообщение с кодом. Дождись пока оно дойдет и отправь сюда.",
                                message_id=edit_message_id, reply_markup=return_menu_keyboard)


@dp.message_handler(state=AddAccountState.GET_CODE_ACCOUNT)
async def _(msg: types.Message, state: FSMContext):
    code = msg.text

    del_message_id = msg.message_id
    state_data = await state.get_data()
    edit_message_id = state_data["message_id"]
    phone_code_hash = state_data["phone_code_hash"]

    name = state_data["name"]
    api_id = state_data["api_id"]
    api_hash = state_data["api_hash"]
    phone = state_data["phone"]
    authorization_password = state_data["authorization_password"]

    client = TelegramClient(f"sessions/{name}_{msg.from_user.id}", api_id, api_hash)

    # print("Connected")
    try:
        await client.connect()
        try:
            await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
            # print("Signed!")
        except SessionPasswordNeededError:
            await client.sign_in(password=authorization_password)

        # print("Sending messages")
        #for admin_id in data.config.ADMINS:
        #    await client.send_message(int(admin_id), "Аккаунт успешно добавлен!")
        # print("Messages was send")

        await bot.delete_message(chat_id=msg.from_user.id, message_id=del_message_id)
        await bot.edit_message_text(chat_id=msg.from_user.id,
                                    text=f"<b>👀 Аккаунт успешно добавлен!</b>\n\nНазвание: {name}\nТелефон: {phone}\n2FA: {authorization_password}\nAPI: <code>{api_id}:{api_hash}</code>",
                                    message_id=edit_message_id, reply_markup='')

        await state.reset_state(with_data=False)
        await client.disconnect()

    except Exception as e:
        print(e)
        await bot.edit_message_text(chat_id=msg.from_user.id,
                                    text=f"<b>👀 Добавить аккаунт</b>\n\nПроизошла <b>ошибка</b>. Видимо вы ошиблись в авторизационных данных и/или на аккаунт наложены ограничения. \n\nНазвание: {name}\nТелефон: {phone}\n2FA: {authorization_password}\nAPI: <code>{api_id}:{api_hash}</code>",
                                    message_id=edit_message_id, reply_markup='')
