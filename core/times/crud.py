from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Times
from .times_models import UserTimes


async def get_times_via_tabnum(session: AsyncSession, tabnum: int) -> dict | None:
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{tabnum} not found",
        )
    if user.last_checkout + timedelta(days=1) > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="too small time processed",
        )
    if not user:
        return False

    date = datetime.now()
    time = Times(user=user.id, checkout_time=date)
    user.last_checkout = date
    session.add(time)
    await session.commit()
    return user
