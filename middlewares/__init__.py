from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .language import ACLMiddleware
from data.config import I18N_DOMAIN, LOCALES_DIR


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())


def setup_languages(dp: Dispatcher):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
