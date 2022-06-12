from typing import Optional, Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from utils.db_api.crud import UserCRUD


async def get_lang(user_id: int):
    user = await UserCRUD.get(user_id=user_id)
    if user:
        return user.locale


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale
