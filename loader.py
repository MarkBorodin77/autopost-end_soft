from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api import Sqlite

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
db = Sqlite("database.db")
dp = Dispatcher(bot, storage=storage)