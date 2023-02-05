import asyncio

import aioschedule as schedule
from aiogram import executor
import middlewares, filters, handlers
from loader import dp
from utils.set_bot_commands import set_default_commands


async def scheduler():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды

    asyncio.create_task(scheduler())

    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    #await on_startup_notify(dispatcher)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)