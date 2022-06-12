from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from data.config import CONFIG


DATABASE_URL: str = f"{CONFIG['database']['username']}:{CONFIG['database']['password']}@" \
                    f"{CONFIG['database']['host']}:{CONFIG['database']['port']}/" \
                    f"{CONFIG['database']['name']}"


engine = create_async_engine(f"postgresql+asyncpg://{DATABASE_URL}")


def create_session(func):
    async def wrapper(**kwargs):
        async with AsyncSession(bind=engine) as session:
            return await func(**kwargs, session=session)
    return wrapper
