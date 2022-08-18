from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
	GetCryptoCurrency = State()
	GetCryptoCurrencyTotal = State()
	GetCurrencyFinally = State()
	GetCurrency = State()
	GetWallet = State()
	Apply = State()
	Mail = State()
	Waterloo = State()
