from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat

from keyboards.inline import return_menu_btn, right_action_btn, left_action_btn, continue_setup_btn, \
    select_all_chats_btn, continue_setup_keyboard
from loader import dp, db


@dp.callback_query_handler(lambda c: c.data == "setup_chat")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    if "account_name" not in state_data:
        await query.answer("Ты не выбрал аккаунт!", show_alert=True)
        return 0

    account_name = state_data["account_name"]
    client = TelegramClient(f"sessions/{account_name}", 12345, "ABCDEF")

    account_chats = [{}]
    selected_chats = {}

    row_numbers = 1
    row_number_now = 1
    sch = 0

    async with client:
        for dialog in await client.get_dialogs():
            if (isinstance(dialog.entity, Channel) and dialog.entity.megagroup == True) or (isinstance(dialog.entity, Chat)):
                if sch >= 5:
                    account_chats.append({})
                    row_numbers += 1
                    sch = 0

                account_chats[row_numbers - 1][dialog.id] = dialog.title
                sch += 1


    await state.update_data(row_numbers=row_numbers, row_number_now=row_number_now, account_chats=account_chats,
                            selected_chats=selected_chats)

    await db.update_tables_sql(state)


    chats_keyboard = await get_chats_keyboard(state)



    await query.message.edit_text(
        "<b>⚙ Настроить чаты</b>\n\nНиже в удобной форме приведен список чатов для настройки.",
        reply_markup=chats_keyboard)


async def get_chats_keyboard(state):
    state_data = await state.get_data()

    row_numbers = state_data["row_numbers"]
    row_number_now = state_data["row_number_now"]
    account_chats = state_data["account_chats"]
    selected_chats = state_data["selected_chats"]

    selected_chats_names = []


    chats_keyboard = InlineKeyboardMarkup(row_width=3)

    for chat_id in account_chats[row_number_now - 1].keys():
        chat_title = account_chats[row_number_now - 1][chat_id]

        if chat_id in selected_chats.keys():
            chat_title += " ✅"
            selected_chats_names.append(chat_title)

        chat_btn = InlineKeyboardButton(f"{chat_title}", callback_data=f"setup_chat_{chat_id}")
        chats_keyboard.add(chat_btn)

    row_number_btn = InlineKeyboardButton(f"[{row_number_now}/{row_numbers}]", callback_data="_")

    chats_keyboard.row(left_action_btn, row_number_btn, right_action_btn)
    chats_keyboard.add(select_all_chats_btn)
    chats_keyboard.add(continue_setup_btn)
    chats_keyboard.add(return_menu_btn)

    return chats_keyboard


async def move_action(action, query, state):
    state_data = await state.get_data()

    row_numbers = state_data["row_numbers"]
    row_number_now = state_data["row_number_now"]

    if action == "left":
        if row_number_now <= 1:
            await query.answer("Ты итак уже в самом начале!", show_alert=True)
            return 0

        row_number_now -= 1
    elif action == "right":
        if row_numbers == row_number_now:
            await query.answer("Ты итак уже в самом конце!", show_alert=True)
            return 0

        row_number_now += 1

    await state.update_data(row_number_now=row_number_now)


@dp.callback_query_handler(lambda c: c.data == "right_action")
async def _(query: types.CallbackQuery, state: FSMContext):
    if await move_action("right", query, state) == 0: return 0

    chats_keyboard = await get_chats_keyboard(state)

    await query.message.edit_reply_markup(reply_markup=chats_keyboard)


@dp.callback_query_handler(lambda c: c.data == "left_action")
async def _(query: types.CallbackQuery, state: FSMContext):
    if await move_action("left", query, state) == 0: return 0

    chats_keyboard = await get_chats_keyboard(state)

    await query.message.edit_reply_markup(reply_markup=chats_keyboard)

#TODO Пофиксить отправку сообщений


@dp.callback_query_handler(Text(startswith="setup_chat_"))
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    account_chats = state_data["account_chats"]
    row_number_now = state_data["row_number_now"]
    selected_chats = state_data["selected_chats"]

    selected_chat_id = int(query.data.replace("setup_chat_", ""))

    selected_chat_title = account_chats[row_number_now - 1][selected_chat_id]

    if selected_chat_id in selected_chats.keys():
        del selected_chats[selected_chat_id]
    else:
        selected_chats[selected_chat_id] = selected_chat_title

    await state.update_data(selected_chats=selected_chats)

    text = ""

    for chat_id in selected_chats:
        chat_title = selected_chats[chat_id]
        text += f"\n• {chat_title}"

    if text == "": text = "чаты не выбраны."


    chats_keyboard = await get_chats_keyboard(state)

    await query.message.edit_text(f"<b>⚙ Настроить чаты</b>\n\nВыбранные чаты: {text}", reply_markup=chats_keyboard)




@dp.callback_query_handler(lambda c: c.data == "select_all_chats")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    account_chats = state_data["account_chats"]
    row_number_now = state_data["row_number_now"]
    selected_chats = state_data["selected_chats"]

    #print(selected_chats.keys())

    for array in account_chats:
        for chat_id in array.keys():
            if chat_id not in selected_chats.keys():
                selected_chats[chat_id] = array[chat_id]

    await state.update_data(selected_chats=selected_chats)

    await query.message.edit_text("⚙️ Настроить чаты\n\nВыбраны все чаты.")
    await query.message.edit_reply_markup(reply_markup=continue_setup_keyboard)
