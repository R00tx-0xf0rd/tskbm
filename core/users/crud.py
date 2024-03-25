import datetime

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import User

from data_models import UserModel, BaseUserModel, AllUsersModel
from core.times.crud import create_checkout_time_for_user


async def get_all_users(session: AsyncSession) -> list[BaseUserModel]:
    query = select(User).order_by(User.column)
    result = await session.execute(query)
    users = result.scalars().all()
    print(users)
    models = [BaseUserModel.model_validate(user) for user in users]
    # mdls = AllUsersModel.model_validate(users)
    return models


async def get_user_by_tabnum(
    session: AsyncSession, tabnum: int
) -> BaseUserModel | None:
    query = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(query)
    user = result.scalar()
    if user:
        return BaseUserModel.model_validate(user)
    return None


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
