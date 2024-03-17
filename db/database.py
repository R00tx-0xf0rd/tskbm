from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tskbm.db.models.tables import Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


url = "sqlite+aiosqlite:///db.sqlite"
engine = create_async_engine(url, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)
