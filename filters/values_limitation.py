from aiogram.dispatcher import FSMContext
from loader import bot


class LimitationValue(object):
    VALUES_LIMITATION: dict = {
        'Bitcoin': 0.0005,
        'Ethereum': 0.0175,
        'Dogecoin': 0,
        'Litecoin': 0.01,
    }

    @staticmethod
    async def limitation(state: FSMContext):
        data = await state.get_data()
        if float(data['cryptocurrencytotal']) >= LimitationValue.VALUES_LIMITATION.get(data['cryptocurrency']):
            return await state.set_data()



