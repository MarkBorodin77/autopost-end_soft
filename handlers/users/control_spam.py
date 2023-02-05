import asyncio
import json

import aioschedule as schedule
from aiogram import types
from aiogram.dispatcher import FSMContext
from telethon import TelegramClient
from telethon.errors import FloodWaitError

import data.config
from keyboards.inline import control_spam_keyboard, return_menu_keyboard
from loader import dp, db, bot


async def stop_spam():
    schedule.clear()


async def send_mailing(chats_data, account_name):
    client = TelegramClient(f"sessions/{account_name}", 12345, "ABCDEF", flood_sleep_threshold=0)

    async with client:
        for chat_id in chats_data.keys():
            text = chats_data[chat_id][0]
            photo_ids = chats_data[chat_id][1]
            if photo_ids is None:
                try:
                    await client.send_message(chat_id, text, parse_mode=types.ParseMode.HTML)
                    await asyncio.sleep(0.1)
                except FloodWaitError as e:
                    for admin in data.config.ADMINS:
                        await bot.send_message(admin,

                                               f"➖ Аккаунт {account_name} получил FloodWaitError. Остановлен на {e.seconds}")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    for admin in data.config.ADMINS:
                        await bot.send_message(admin,
                                               f"➖ У аккаунта {account_name} произошла ошибка. Код ошибки: {e.args}.")


            else:
                photos = []

                for photo_name in photo_ids:
                    photos.append(f"photos/{photo_name}.jpg")

                try:
                    await client.send_file(entity=chat_id, caption=text, file=photos, parse_mode=types.ParseMode.HTML)
                    await asyncio.sleep(0.1)
                except Exception as e:
                    for admin in data.config.ADMINS:
                        await bot.send_message(admin,
                                               f"➖ У аккаунта {account_name} произошла ошибка. Код ошибки: {e.args}.")


async def start_mailing(chats_data, account_name):
    # print("Start Mailing")

    sorted_chats_data = {}
    '''{
        time: {
                chat_id: [text, photo_id]
                chat_id: [text, photo_id]  
            }
        }
    }'''

    schedule.clear()

    for chat_data in chats_data:
        chat_id = chat_data[0]
        times = json.loads(chat_data[2])
        html_text = chat_data[3]
        photo_id = json.loads(chat_data[4])

        if str(photo_id[0]) == "None":
            photo_id = None

        for time in times:

            if time not in sorted_chats_data.keys():
                sorted_chats_data[time] = {}

            sorted_chats_data[time][chat_id] = [html_text, photo_id]

            # schedule.every().day.at(time).do(send_mailing, chat_id=chat_id, text=html_text, account_name=account_name).tag(chat_id)

    # print(sorted_chats_data)

    for time in sorted_chats_data.keys():
        schedule.every().day.at(time).do(send_mailing, sorted_chats_data[time], account_name)

    return len(chats_data)


@dp.callback_query_handler(lambda c: c.data == "control_spam")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    if "account_name" not in state_data:
        await query.answer("Ты не выбрал аккаунт!", show_alert=True)
        return 0

    await query.message.edit_text(
        "<b>⛔ Контроль спама</b>\n\n🟢 — Запускает только во включенные чаты\n🔥 — Запускает по всем чатам\n🚫 — Останавливает весь спам",
        reply_markup=control_spam_keyboard)


@dp.callback_query_handler(lambda c: c.data == "start_working_spam")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    account_name = state_data["account_name"]

    chats_data = await db.get_working_chats_sql(state)

    chats_length = await start_mailing(chats_data, account_name)

    await query.message.edit_text(f"<b>🟢 Спам запущен во включенные чаты</b>\n\nТочное количество: {chats_length}",
                                  reply_markup=return_menu_keyboard)


@dp.callback_query_handler(lambda c: c.data == "start_all_spam")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    account_name = state_data["account_name"]

    chats_data = await db.get_all_chats_sql(state)

    chats_length = await start_mailing(chats_data, account_name)

    await query.message.edit_text(f"<b>🔥 Спам запущен во все чаты</b>\n\nТочное количество: {chats_length}",
                                  reply_markup=return_menu_keyboard)


@dp.callback_query_handler(lambda c: c.data == "stop_all_spam")
async def _(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    account_name = state_data["account_name"]

    chats_data = await db.get_all_chats_sql(state)

    await stop_spam()

    await query.message.edit_text(f"<b>🚫 Остановить весь спам</b>\n\nРассылка по всем чатам на аккаунте остановлена.",
                                  reply_markup=return_menu_keyboard)
