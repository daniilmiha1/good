from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import main_menu
from keyboards.inline import languages
from loader import dp, _
from utils.db_api.crud import UserCRUD
from utils.misc import rate_limit


@rate_limit(limit=60)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(_('Привет, {}!').format(message.from_user.full_name))
    await message.answer(_('Полетели!'), reply_markup= await main_menu())


@dp.message_handler(text="language")
async def send_languages(message: types.Message):
    await message.delete()
    await message.answer(
        text="Choice Language",
        reply_markup=await languages()
    )


@dp.callback_query_handler(lambda call: call.data.startswith("language_"))
async def get_language(call: types.CallbackQuery):
    locale = call.data.split("_")[-1]
    await UserCRUD.add(
        user_id=call.from_user.id,
        locale=locale
    )
    await call.message.edit_text("Done")
    await call.message.edit_reply_markup(None)


@dp.message_handler(
    content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
async def get_audio(message: types.Message):
    await message.delete()
