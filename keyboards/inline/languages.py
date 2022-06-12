from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.crud import LanguageCRUD


async def languages() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=3).add(*[
        InlineKeyboardButton(text=language.name, callback_data=f"language_{language.name}")
        for language in await LanguageCRUD.get_all()
    ])
