from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from middlewares import setup_languages

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

i18n = setup_languages(dp)
_ = i18n.gettext

# Создадим псевдоним для метода gettext, чтобы получать текст с нужным переводом

# translation = i18n.gettext