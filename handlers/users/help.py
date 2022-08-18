from aiogram import types

from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=60)
@dp.message_handler(text='help')
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        'start - Начать работу',
        'help - Получить помощь',
        'about - Получить информацию про нас',
        'buycrypto - Купить криптовалюту',
        'Выберите нужную вам команду для работы с ботом.',
        'При возникновении вопросов, обращайтесь в службу поддержки пользователей @businamih.'
    ]
    await message.answer(_('\n'.join(text)))