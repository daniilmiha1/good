from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db_api.models import Language
from utils.db_api.engine import create_session


class LanguageCRUD(object):

    @staticmethod
    @create_session
    async def add(language: str, session: AsyncSession = None) -> bool:
        session.add(Language(name=language))
        try:
            await session.commit()
        except IntegrityError:
            return False
        else:
            return True

    @staticmethod
    @create_session
    async def get_all(session: AsyncSession = None) -> list[Language]:
        languages = await session.execute(
            select(Language)
        )
        if languages:
            return [language[0] for language in languages]
        