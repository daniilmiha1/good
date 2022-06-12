from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from data.config import I18N_DOMAIN, LOCALES_DIR
#pybabel update -d locales -D testbot -i locales/testbot.pot


# class ACLMidlleware(I18nMiddleware):
#         async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
#                 user = types.User.get_current()
#                 return await get_lang(user.id) or user.locale
#
# def setup_middleware(dp):
#         i18n = ACLMidlleware(I18N_DOMAIN, LOCALES_DIR)
#         dp.middleware.setup(i18n)
#         return i18n
#
# LANGUAGE_CHOICE = ('English', 'Russian', 'Belarusian')
#
# @dp.message_handler(text="language", state=None)
# async def select_language(message: types.Message):
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*LANGUAGE_CHOICE)
#         message.text = choisen_text
#         await message.answer("Выберите язык/Select a language", reply_markup=keyboard)
#
#         if message.text in LANGUAGE_CHOICE:
#                 await message.answer(
#                         "Такого языка нет, воспользуйтесь клавиатурой/There is no such language, use the keyboard",
#                         reply_markup=keyboard)
#         else:
#             await message.answer("Такого языка нет, воспользуйтесь клавиатурой/There is no such language, use the keyboard", reply_markup=keyboard)