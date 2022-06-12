from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.db_api.models import User
from utils.db_api.engine import create_session


class UserCRUD(object):

    @staticmethod
    @create_session
    async def add(user_id: int, locale: str, session: AsyncSession = None) -> bool:
        user = await session.execute(select(User).where(User.id == user_id))
        try:
            user = user.first()[0]
        except TypeError:
            user = User(
                id=user_id,
                locale=locale
            )
            session.add(user)
            await session.commit()
        else:
            await session.execute(
                update(User).where(User.id == user_id).values(locale=locale)
            )
            await session.commit()

    @staticmethod
    @create_session
    async def get(user_id: int, session: AsyncSession = None) -> Optional[User]:
        user = await session.execute(
            select(User).where(User.id == user_id)
        )
        try:
            return user.first()[0]
        except TypeError:
            return None

