from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api.user import User


class GetDBUser(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        data["user"] = User(id=666, name=message.from_user.full_name)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        data["user"] = User(id=666, name=cq.message.from_user.full_name)