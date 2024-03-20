from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Times
from .times_models import UserTimes, Period


async def get_times_via_tabnum(session: AsyncSession, tabnum: int):
    # stmt = select(User).filter(and_(User.tabnum == tabnum, Times.user == User.id))
    stmt = select(User).filter(User.tabnum == tabnum)
    result = await session.execute(stmt)
    periods = result.scalar()
    model = UserTimes.model_validate(periods)
    return UserTimes.model_dump_json(model)
