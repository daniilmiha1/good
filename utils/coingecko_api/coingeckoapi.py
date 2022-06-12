from aiohttp import ClientSession

from data.config import CONFIG


class CoinGeckoAPI(object):
    BASE_URI = 'https://api.coingecko.com'

    def __init__(self) -> None:
        self.__api_key: str = CONFIG['currency']['API_KEY']
        self.__secret_key: str = CONFIG['currency']['SECRET_KEY']

    @staticmethod
    async def get_simple_price(token: str, currency: str) -> dict:
        async with ClientSession(base_url=CoinGeckoAPI.BASE_URI) as session:
            response = await session.get(
                url='/api/v3/simple/price/',
                params={
                    'ids': token,
                    'vs_currencies': currency
                }
            )
            return await response.json()
