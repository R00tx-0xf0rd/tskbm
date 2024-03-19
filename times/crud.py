from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Times


async def get_times_via_tabnum(session: AsyncSession, tabnum: int):
    stmt = select(User.times).filter(and_(User.tabnum == tabnum, Times.user == User.id))
    result = await session.execute(stmt)
    times = result.scalars().all()
    return times
