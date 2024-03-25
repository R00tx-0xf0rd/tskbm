from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Times
from .times_models import UserTimes, Period


async def get_times_via_tabnum(session: AsyncSession, tabnum: int) -> dict:
    # stmt = select(User).filter(and_(User.tabnum == tabnum, Times.user == User.id))
    stmt = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(stmt)
    periods = result.scalar()
    model = UserTimes.model_validate(periods)
    return UserTimes.model_dump(model)


async def create_checkout_time_for_user(
    session: AsyncSession, tabnum: int
) -> (bool, Times):
    query = select(User.id).filter(User.tabnum == tabnum)
    result = await session.execute(query)
    user_id = result.scalar()
    if not user_id:
        return False

    time = Times(user=user_id, checkout_time=datetime.now())
    session.add(time)
    res = True
    try:
        await session.commit()
    except IntegrityError:
        res = False
    finally:
        # await session.rollback()
        return res
