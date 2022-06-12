from aiogram import types

from loader import dp, _


@dp.message_handler(text="about", state=None)
async def bot_about(message: types.Message):
    text = [
        'C 2019 года активно занимаемся добычей и продажей цифровой валюты.',
        'Данный обменник поможет вам сделать транзакцию анонимно.',
        'Рассмотрение заявки от 30 минут до 8 часов.',
        'На сегодня имеем более 1000 довольных клиентов.'
    ]
    await message.answer(_('\n'.join(text)))