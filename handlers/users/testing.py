from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from keyboards.inline.languages import waterloo
from loader import dp, _
from states import Test
from utils.coingecko_api import CoinGeckoAPI
from utils.blockcyper_api import BlockCyperApi
from email_sending.email_send import send_email
from filters import LimitationValue
from aiogram_calendar import DialogCalendar, dialog_cal_callback

CRYPTOCURRENCY = ('Bitcoin', 'Ethereum', 'Dogecoin', 'Litecoin')
CURRENCY = ('RUB', 'USD', 'BYN')
CRYPTO = ('Узнавать полезную информацию о крипте', 'Нет')


@dp.message_handler(text='buycrypto')
async def enter_test(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*CRYPTOCURRENCY)

    # await state.update_data(currency=message.text)

    await message.answer(
        "Какую криптовалюту вы бы хотели получить?",
        reply_markup=keyboard)

    await Test.GetCryptoCurrency.set()


# @dp.message_handler(Text(equals='Bitcoin'))
# async def get_btc(message: types.Message):


@dp.message_handler(state=Test.GetCryptoCurrency)
async def get_cryptocurrency(message: types.Message, state: FSMContext):
    if message.text in CRYPTOCURRENCY:

        await state.update_data(cryptocurrency=message.text)

        await message.answer(_("Введите какое количество вам нужно(При бездействии бота введите повторно)"), reply_markup=types.ReplyKeyboardRemove())

        await Test.GetCryptoCurrencyTotal.set()
    else:
        await message.answer(text='Такой криптовалюты нет, воспользуйтесь клавиатурой!')


# @dp.message_handler(state=Test.GetCryptoCurrencyTotal)
# async def get_cryptocurrency_total(message: types.Message, state: FSMContext):
#     answer = message.text.replace(',', '.')
#     try:
#         answer = float(answer)
#
#         await state.update_data(cryptocurrencytotal=answer)
#
#         await Test.GetCurrency.set()
#
#     except ValueError:
#         await message.answer(text='Неверное количество, введите число')


@dp.message_handler(state=Test.GetCryptoCurrencyTotal)
async def apply_limit(message: types.Message, state: FSMContext):
    answer = message.text.replace(',', '.')
    try:
        answer = float(answer)

        await state.update_data(cryptocurrencytotal=answer)

        # await Test.GetCurrency.set()

    except ValueError:
        await message.answer(text='Неверное количество, введите число')
    str(message.text.replace(',', '.'))
    data = await state.get_data()
    if data["cryptocurrency"] == 'Bitcoin' and float(data["cryptocurrencytotal"]) >= 0.0005:
        await state.update_data(cryptocurrencytotal=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*CURRENCY)

        await message.answer("Выберите валюту которой будете расплачиваться", reply_markup=keyboard)

        await Test.GetCurrencyFinally.set()
    elif data["cryptocurrency"] == 'Ethereum' and float(data["cryptocurrencytotal"]) >= 0.0175:
        await state.update_data(cryptocurrencytotal=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*CURRENCY)

        await message.answer("Выберите валюту которой будете расплачиваться", reply_markup=keyboard)

        await Test.GetCurrencyFinally.set()
    elif data["cryptocurrency"] == 'Litecoin' and float(data["cryptocurrencytotal"]) >= 0.01:
        await state.update_data(cryptocurrencytotal=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*CURRENCY)

        await message.answer("Выберите валюту которой будете расплачиваться", reply_markup=keyboard)

        await Test.GetCurrencyFinally.set()
    elif data["cryptocurrency"] == 'Dogecoin' and float(data["cryptocurrencytotal"]) > 0:
        await state.update_data(cryptocurrencytotal=float(message.text))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*CURRENCY)

        await message.answer("Выберите валюту которой будете расплачиваться", reply_markup=keyboard)

        await Test.GetCurrencyFinally.set()
    else:
        await message.answer('Минимальная величина транзакции биткоина 0.0005, эфира 0.0175, лайткоина 0.01, догекоина больше 0, введите пожалуйста корректное значение')
        await state.update_data(cryptocurrencytotal=message.text)


@dp.message_handler(state=Test.GetCurrencyFinally)
async def get_currency(message: types.Message, state: FSMContext):
    if message.text in CURRENCY:

        await state.update_data(currency=message.text)

        await message.answer(_("Введите ваш криптокошелёк"), reply_markup=types.ReplyKeyboardRemove())

        await Test.GetWallet.set()
    else:
        await message.answer(
            text='Неверные данные, воспользуйтесь клавиатурой!'
        )


@dp.message_handler(state=Test.GetWallet)
async def get_wallet(message: types.Message, state: FSMContext):
    await state.update_data(wallet=message.text)
    data = await state.get_data()
    if data['cryptocurrency'].lower() == 'ethereum' and 40 <= len(message.text) <= 44:
        await message.answer(_(f"Спасибо за ваши ответы, ваша заявка на рассмотрении.\n\n"
                               f"Вы хотите {data['cryptocurrencytotal']} {data['cryptocurrency']} \n\n"
                               f"Будете платить {data['currency']}\n\n"
                               f"Выплату получите на кошелек {message.text}\n\n"
                               f"Всё верно?"))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(_('Да'))
        await message.answer(_("Подтвердите данные или начните работу заново"), reply_markup=keyboard)
        # await smtpObj.login(CONFIG["gmail"]["mail"], CONFIG["gmail"]["password"])
        await Test.Apply.set()
    elif await BlockCyperApi.get_wallet(state):
        await message.answer(_(f"Спасибо за ваши ответы, ваша заявка на рассмотрении.\n\n"
                               f"Вы хотите {data['cryptocurrencytotal']} {data['cryptocurrency']} \n\n"
                               f"Будете платить {data['currency']}\n\n"
                               f"Выплату получите на кошелек {message.text}\n\n"
                               f"Всё верно?"))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(_('Да'))
        await message.answer(_("Подтвердите данные или начните работу заново"), reply_markup=keyboard)
        await Test.Apply.set()
        await state.update_data(apply=message.text)
    else:
        await message.answer('Введите корректный кошелек')


@dp.message_handler(text='Да', state=Test.Apply)
async def plata(message: types.Message, state: FSMContext):
    MY_WALLETS: dict = {
        'usd': 4177531158632524,
        'rub': 4276590017537092,
        'byn': 123,
    }

    data = await state.get_data()

    if data['currency'].lower() == 'byn':
        await state.update_data(currency="rub")
        response = await CoinGeckoAPI.get_simple_price(data['cryptocurrency'], "rub")
        currency_price = float(response[data['cryptocurrency'].lower()]["rub"]) *float( data['cryptocurrencytotal']) * float(1.25) * float(0.033)
    else:
        response = await CoinGeckoAPI.get_simple_price(data['cryptocurrency'], data['currency'])
        currency_price = float(response[data['cryptocurrency'].lower()][data['currency'].lower()]) * float(data[
            'cryptocurrencytotal']) * float(1.2)
    await state.update_data(currency_price=currency_price)

    await message.answer(
        _(f'Переведите {round(currency_price, 2)} {data["currency"].upper()}, по номеру карты {MY_WALLETS.get(data["currency"].lower())}\n\n'
          f'После перевода подтвердите платеж'))

    await Test.Mail.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(_('Подтвердить платеж'))
    await message.answer(
        _("Внимание, отправляйте только точную сумму, при переводе неточной суммы обменник имеет право отказаться от сделки."),
        reply_markup=keyboard)


# @dp.message_handler(text='Подтвердить платеж', state=Test.Mail)
# async def accept(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     await state.finish()
#     await message.answer(_(
#         "Ваша заявка в очереди, обычно перевод занимает не более 30 минут, но при загруженности блокчейна это может доходить и до 8 часов."),
#         reply_markup=await DialogCalendar().start_calendar())
#     await send_email(data)
#     await Test.Waterloo.set()

# start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
# start_kb.row('Navigation Calendar', 'Dialog Calendar')
#
# @dp.callback_query_handler(dialog_cal_callback.filter())
# async def process_dialog_calendar(callback: types.CallbackQuery, callback_data: dict):
#     selected, date = await DialogCalendar().process_selection(callback, callback_data)
#     if selected:
#         await callback.message.answer(
#             f'You selected {date.strftime("%d/%m/%Y")}',
#             reply_markup=start_kb
#         )

    # await message.answer(f"")
    # await message.answer(f"")
