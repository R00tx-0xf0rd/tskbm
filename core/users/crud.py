import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.times.crud import create_checkout_time_for_user
from data_models import BaseUserModel
from db import User


async def get_all_users(session: AsyncSession) -> list[User]:
    query = select(User).order_by(User.column)
    result = await session.execute(query)
    users = result.scalars().all()
    return list(users)


async def get_col(session: AsyncSession, col: int) -> list[dict]:
    stmt = select(User).filter(User.column == col)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return [BaseUserModel.model_validate(user).model_dump() for user in users]


async def get_user_by_tabnum(
        session: AsyncSession,
        tabnum: int
) -> User | None:
    query = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(query)
    return result.scalar()


async def create_user(session: AsyncSession, user_in: User) -> int:
    user_in.last_checkout = datetime.datetime.now()
    session.add(user_in)
    try:
        await session.commit()
    except IntegrityError as e:
        print(e)
        # await session.rollback()
        return 0
    if await create_checkout_time_for_user(session, user_in.tabnum):
        return user_in.id


async def get_id_by_tabnum(session: AsyncSession, tabnum: int) -> int:
    stmt = select(User.id).filter(User.tabnum == tabnum)
    result = await session.execute(stmt)
    id = result.scalar()
    return id
