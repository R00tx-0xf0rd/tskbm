import datetime

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from db import User, Times
from db import Watch

from data_models import UserModel, BaseUserModel, AllUsersModel


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
    # async with new_session() as session:
    # session.get(User).filter(tabnum == tabnum)
    query = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(query)
    user = result.scalar()
    if user:
        return BaseUserModel.model_validate(user)
    return None


async def add_watch(session: AsyncSession, serial_number: str) -> int:
    watch = Watch(ser_num=serial_number)
    session.add(watch)
    await session.commit()
    return watch.id


async def attach_watches_to_user_by_tabnum(
    session: AsyncSession, tabnum_in: int, watch_serial: str
) -> bool:
    stmt = select(User).filter(User.tabnum == tabnum_in)
    result = await session.execute(stmt)
    user = result.scalar()
    if not user:
        return False
    stmt = select(Watch.id).filter(Watch.ser_num == watch_serial)
    result = await session.execute(stmt)
    wid = result.scalar()
    if not wid:
        return False
    user.watch_id = wid
    session.add(user)
    await session.commit()
    return True


async def create_user(session: AsyncSession, user_in: User) -> int:
    user_in.last_checkout = datetime.datetime.now()
    session.add(user_in)
    try:
        await session.commit()
    except IntegrityError as e:
        print(e)
        # await session.rollback()
        return 0
    if await create_checkout_time_for_user(session, user_in.id):
        return user_in.id


async def create_checkout_time_for_user(session: AsyncSession, user_id: int) -> bool:
    time = Times(user=user_id, checkout_time=datetime.datetime.now())
    session.add(time)
    res = True
    try:
        await session.commit()
    except IntegrityError:
        res = False
    finally:
        # await session.rollback()
        return res


async def get_id_by_tabnum(session: AsyncSession, tabnum: int) -> int:
    stmt = select(User.id).filter(User.tabnum == tabnum)
    result = await session.execute(stmt)
    id = result.scalar()
    return id
