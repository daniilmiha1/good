import logging
from keyboards.default import client

from aiogram import Dispatcher

from data.config import admins


async def on_startup_notify(dp: Dispatcher):
    
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе", reply_markup=client.main_command)

        except Exception as err:
            logging.exception(err)
