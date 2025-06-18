from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from env import Env



class DataBase:
    url = f"postgresql+asyncpg://{Env.user}:{Env.password}@{Env.host}/{Env.db_name}"
    engine = create_async_engine(url, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    @classmethod
    async def check_connection(cls):
        try:
            async with cls.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            print("✅ Успешное подключение к БД")
        except SQLAlchemyError as e:
            print(f"❌ Ошибка подключения к БД: {e}")
