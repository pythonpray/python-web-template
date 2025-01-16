from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from settings.config import get_settings

database = get_settings().database
engine: AsyncEngine = create_async_engine(
    database.database_conn_url,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    max_overflow=database.max_overflow,
    pool_size=database.db_pool_size,
)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
