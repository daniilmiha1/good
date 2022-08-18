from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

a_1 = KeyboardButton('/start')
main_command = ReplyKeyboardMarkup(resize_keyboard=True).add(a_1)

a_2 = KeyboardButton('help')
a_3 = KeyboardButton('about')
a_4 = KeyboardButton('language')
a_5 = KeyboardButton('test')


async def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False
    ).add(*[
        KeyboardButton(text=button)
        for button in ('help', 'about', 'buycrypto')
    ])