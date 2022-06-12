from aiogram import types

from states import Test
from aiogram.dispatcher.storage import FSMContext

from loader import dp, _
from states import Test
from utils.coingecko_api import CoinGeckoAPI

CRYPTOCURRENCY = ('Bitcoin', 'Ethereum', 'Dogecoin', 'Litecoin')
CURRENCY = ('RUB', 'USD', 'BYN')


@dp.message_handler(text='test')
async def enter_test(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*CRYPTOCURRENCY)


    # await state.update_data(currency=message.text)

    await message.answer(_(
        "Какую криптовалюту вы бы хотели получить?"),
        reply_markup=keyboard)

    await Test.GetCryptoCurrency.set()


# @dp.message_handler(Text(equals='Bitcoin'))
# async def get_btc(message: types.Message):


@dp.message_handler(state=Test.GetCryptoCurrency)
async def get_cryptocurrency(message: types.Message, state: FSMContext):
    if message.text in CRYPTOCURRENCY:

        await state.update_data(cryptocurrency=message.text)

        await message.answer(_("Введите какое количество вам нужно"), reply_markup=types.ReplyKeyboardRemove())

        await Test.GetCryptoCurrencyTotal.set()
    else:
        await message.answer(_(text='Такой криптовалюты нет, воспользуйтесь клавиатурой!'))


@dp.message_handler(state=Test.GetCryptoCurrencyTotal)
async def get_cryptocurrency_total(message: types.Message, state: FSMContext):
    if message.text.strip().isdigit():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*CURRENCY)

        await state.update_data(cryptocurrencytotal=int(message.text.strip()))

        await message.answer(_("Какой валютой вы будете платить?"), reply_markup=keyboard)

        await Test.GetCurrency.set()
    else:
        await message.answer(_(text='Неверное количество, введите число!'))


@dp.message_handler(state=Test.GetCurrency)
async def get_currency(message: types.Message, state: FSMContext):
    if message.text in CURRENCY:

        await state.update_data(currency=message.text)

        await message.answer(_("Введите ваш криптокошелёк"), reply_markup=types.ReplyKeyboardRemove())

        await Test.GetWallet.set()
    else:
        await message.answer(_(
            text='Неверные данные, воспользуйтесь клавиатурой!'
        ))


@dp.message_handler(state=Test.GetWallet)
async def get_wallet(message: types.Message, state: FSMContext):
    if len(message.text) != 42:
        await message.answer(_('Введите пожалуйста корректный кошелек'))
    else:
        data = await state.get_data()

        await message.answer(_(f"Спасибо за ваши ответы, ваша заявка на рассмотрении.\n\n"
                         f"Вы хотите {data['cryptocurrency']} {data['cryptocurrencytotal']}\n\n"
                         f"Будете платить {data['currency']}\n\n"
                         f"Выплату получите на кошелек {message.text}\n\n"
                         f"Всё верно?"))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(_('Да'))
        await message.answer(_("Подтвердите данные или начните работу заново"), reply_markup=keyboard)

        await Test.Apply.set()


@dp.message_handler(text='Да', state=Test.Apply)
async def plata(message: types.Message, state: FSMContext):

    MY_WALLETS: dict = {
        'usd': 4177531158632524,
        'rub': 4276590017537092,
        'eur': 1111111111111111,
        'byn': 2222222222222222,
    }

    data = await state.get_data()

    response = await CoinGeckoAPI.get_simple_price(data['cryptocurrency'], data['currency'])
    if data['currency'].lower() == 'byn':
        await state.update_data(currency="rub")
        currency_price = response[data['cryptocurrency'].lower()][data['currency'].lower()] * data['cryptocurrencytotal'] * 1.25 * 0.033
    else:
        currency_price = response[data['cryptocurrency'].lower()][data['currency'].lower()] * data['cryptocurrencytotal'] * 1.25

    await message.answer(_(f'Переведите {round(currency_price, 2)} {data["currency"].upper()}, по номеру карты {MY_WALLETS.get(data["currency"].lower())}\n\n'
                         f'После перевода подтвердите платеж'))
    await state.finish()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(_('Подтвердить платеж'))
    await message.answer(_("Внимание, отправляйте только точную сумму, при переводе неточной суммы обменник имеет право отказаться от сделки."), reply_markup=keyboard)

@dp.message_handler(text='Подтвердить платеж')
async def accept(message: types.Message):
    await message.answer(_(
        "Ваша заявка в очереди, обычно перевод занимает не более 30 минут, но при загруженности блокчейна это может доходить и до 8 часов."),
        reply_markup=types.ReplyKeyboardRemove())

    # await message.answer(f"")
    # await message.answer(f"")
