from pprint import pprint

from currencycom.client import Client

client = Client('1BkoTX1Qlt3mnf69', 'uy6%60-J9DD~peHI+U0wJ:n:0ApmE^HK')

exchange_info = client.get_exchange_info()
tradable_symbols = [x['byn'] for x in exchange_info['symbols']]
pprint(tradable_symbols,
       indent=2)