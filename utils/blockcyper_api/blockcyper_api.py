import aiohttp
import asyncio

from aiogram.dispatcher import FSMContext


class BlockCyperApi(object):
    MY_COINS: dict = {
        'Bitcoin': 'btc',
        'Dogecoin': 'doge',
        'Litecoin': 'ltc',
    }

    @staticmethod
    async def get_wallet(state: FSMContext):
        async with aiohttp.ClientSession() as session:
            data = await state.get_data()
            response = await session.get(f'https://api.blockcypher.com/v1/{BlockCyperApi.MY_COINS.get(data["cryptocurrency"])}/main/addrs/{data["wallet"]}')
            if response.status == 200:
                return await response.json()
                # print("Status:", response)
                # print("Status:", response.status)
                # print("Content-type:", response.headers['content-type'])
