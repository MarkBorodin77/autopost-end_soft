from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import ADMINS


class AdminMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    async def on_process_message(self, msg: types.Message, data: dict):
        user_id = str(msg.from_user.id)

        if user_id not in ADMINS:
            await msg.answer("<b>❌ Запросите доступ у администратора!</b>")
            raise CancelHandler()

