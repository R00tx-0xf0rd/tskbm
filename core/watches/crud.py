from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Watch


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
