import json
from pathlib import Path


def load_config() -> dict:
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)


CONFIG = load_config()


BOT_TOKEN = CONFIG['bot']['token']
admins = CONFIG['bot']['admins']

I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'
