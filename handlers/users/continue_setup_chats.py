import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import continue_setup_keyboard, return_setup_chats_menu
from loader import dp, db, bot
from states import SetupChatsState


@dp.callback_query_handler(lambda c: c.data == "continue_setup")
async def continue_setup(query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    state_data = await state.get_data()

    selected_chats = state_data["selected_chats"]
    account_name = state_data["account_name"]

    if len(selected_chats) == 0:
        await query.answer("Ты не выбрал ни один чат!", show_alert=True)
        return 0

    if len(selected_chats) == 1:
        # COMPLETED Показывать данные отдельного чата
        chat_id = list(selected_chats.keys())[0]
        chat_data = await db.get_one_chat_sql(account_name, chat_id)

        chat_title = chat_data[2]
        time = json.loads(chat_data[3])
        work = chat_data[4]
        text = chat_data[5]

        times = ""

        for i in time:
            times += f"{i}, "

        #print(times)

        times = list(times)

        times[-1] = ""
        times[-2] = "."

        times = "".join(times)

        if work == 0:
            work = "❌ Выключено"
        elif work == 1:
            work = "✅ Включено"

        try:
            await query.message.edit_text(
                f"<b>⚙ Настроить чаты</b>\n\n<b>Выбранный чат</b>: {chat_title}\n\n<b>Время рассылки:</b> {times}\n\n<b>Текст:</b>\n{text}\n\n<b>Состояние:</b> {work}",
                reply_markup=continue_setup_keyboard)
        except:
            pass
    try:
        await query.message.edit_reply_markup(reply_markup=continue_setup_keyboard)
    except:
        pass


@dp.callback_query_handler(lambda c: c.data == "edit_time")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    selected_chats = state_data["selected_chats"]
    selected_chats_names = []

    edited_message_id = query.message.message_id
    await state.update_data(message_id=edited_message_id)

    for chat_id in selected_chats.keys():
        selected_chats_names.append(selected_chats[chat_id])

    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await SetupChatsState.EDIT_TIME.set()
    await query.message.edit_text(
        f"<b>🕙 Изменить время</b>\n\nВыбранные чаты: {text}\n\nВведи через энтер время для рассылки сообщения:",
        reply_markup=return_setup_chats_menu)


@dp.message_handler(state=SetupChatsState.EDIT_TIME)
async def _(msg: types.Message, state: FSMContext):
    times = msg.text.split("\n")

    state_data = await state.get_data()

    edited_message_id = state_data["message_id"]
    delete_message_id = msg.message_id

    selected_chats = state_data["selected_chats"]
    await db.update_time_sql(state, times)

    text = ""
    text2 = ""

    # print(selected_chats)

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    for i in times:
        text2 += f"{i}, "

    text2 = text2[:-2]

    await bot.delete_message(msg.from_user.id, delete_message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f"<b>🕙 Изменить время</b>\n\nВыбранные чаты: {text}\n\nУстановленное время рассылки: {text2}.",
                                message_id=edited_message_id, reply_markup=return_setup_chats_menu)


@dp.callback_query_handler(lambda c: c.data == "edit_text")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    selected_chats = state_data["selected_chats"]

    edited_message_id = query.message.message_id
    await state.update_data(message_id=edited_message_id)

    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await SetupChatsState.EDIT_TEXT.set()
    await query.message.edit_text(
        f"<b>✍ Изменить текст</b>\n\nВыбранные чаты: {text}\n\nВведи текст который будет использован для рассылки:",
        reply_markup=return_setup_chats_menu)


@dp.message_handler(state=SetupChatsState.EDIT_TEXT, content_types=types.ContentTypes.TEXT)
async def _(msg: types.Message, state: FSMContext):
    html_text = msg.html_text

    state_data = await state.get_data()

    edited_message_id = state_data["message_id"]
    delete_message_id = msg.message_id

    selected_chats = state_data["selected_chats"]

    await db.update_text_sql(state, html_text)

    text = ""
    text2 = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    sch = 0

    await bot.delete_message(msg.from_user.id, delete_message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f"<b>✍ Изменить текст</b>\n\nВыбранные чаты: {text}\n\n<b>Установленный текст:</b>\n{html_text}",
                                message_id=edited_message_id, reply_markup=return_setup_chats_menu)


@dp.callback_query_handler(lambda c: c.data == "add_photo")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    selected_chats = state_data["selected_chats"]

    edited_message_id = query.message.message_id
    await state.update_data(message_id=edited_message_id)


    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await SetupChatsState.ADD_PHOTO.set()
    await query.message.edit_text(
        f"<b>➕ Добавить фото</b>\n\nВыбранные чаты: {text}\n\nСкинь <b>1 фотографию</b> которую хочешь добавить.",
        reply_markup=return_setup_chats_menu)

@dp.callback_query_handler(lambda c: c.data == "delete_photo")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    selected_chats = state_data["selected_chats"]

    await db.delete_photo_sql(state)

    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await SetupChatsState.ADD_PHOTO.set()
    await query.message.edit_text(
        f"<b>➕ Добавить фото</b>\n\nВыбранные чаты: {text}\n\nВсе фото успешно убраны.",
        reply_markup=return_setup_chats_menu)


@dp.message_handler(state=SetupChatsState.ADD_PHOTO, content_types=types.ContentTypes.PHOTO)
async def _(msg: types.Message, state: FSMContext):
    file_info = await bot.get_file(msg.photo[-1].file_id)
    await bot.download_file_by_id(file_info.file_id, f"photos/{file_info.file_unique_id}.jpg")

    state_data = await state.get_data()

    delete_message_id = msg.message_id


    selected_chats = state_data["selected_chats"]
    edited_message_id = state_data["message_id"]


    await db.add_photo_sql(state, file_info.file_unique_id)

    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await bot.delete_message(msg.from_user.id, delete_message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id,
                                text=f"<b>✍ Изменить текст</b>\n\nВыбранные чаты: {text}\n\nФото добавлено.",
                                message_id=edited_message_id, reply_markup=return_setup_chats_menu)



@dp.callback_query_handler(lambda c: c.data == "mute_chats")
async def _(query: types.CallbackQuery, state: FSMContext):
    await db.mute_chats_sql(state)

    state_data = await state.get_data()
    selected_chats = state_data["selected_chats"]

    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await query.message.edit_text(
        f"<b>❌ Выключить чаты</b>\n\nВыбранные чаты: {text}\n\nВыбранные чаты успешно <b>выключены</b>.",
        reply_markup=return_setup_chats_menu)


@dp.callback_query_handler(lambda c: c.data == "enable_chats")
async def _(query: types.CallbackQuery, state: FSMContext):
    await db.enable_chats_sql(state)

    state_data = await state.get_data()
    selected_chats = state_data["selected_chats"]

    text = ""

    for chat_id in selected_chats.keys():
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."

    await query.message.edit_text(
        f"<b>✅ Включить чаты</b>\n\nВыбранные чаты: {text}\n\nВыбранные чаты успешно <b>включены</b>.",
        reply_markup=return_setup_chats_menu)


@dp.callback_query_handler(lambda c: c.data == "return_back", state="*")
async def _(query: types.CallbackQuery, state: FSMContext):
    await continue_setup(query, state)
