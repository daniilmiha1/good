from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
	GetCryptoCurrency = State()
	GetCryptoCurrencyTotal = State()
	GetCurrency = State()
	GetWallet = State()
	Apply = State()
