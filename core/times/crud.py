from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Times
from .times_models import UserTimes, Period


async def get_times_via_tabnum(session: AsyncSession, tabnum: int) -> dict | None:
    # stmt = select(User).filter(and_(User.tabnum == tabnum, Times.user == User.id))
    stmt = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(stmt)
    periods = result.scalar()
    if not periods:
        return None
    model = UserTimes.model_validate(periods)
    return UserTimes.model_dump(model)


async def create_checkout_time_for_user(
    session: AsyncSession, tabnum: int
) -> (bool, Times):
    query = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(query)
    user = result.scalar()
    if not user:
        return False

    date = datetime.now()
    time = Times(user=user.id, checkout_time=date)
    user.last_checkout = date
    session.add(time)
    await session.commit()
    return user

