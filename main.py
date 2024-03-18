import asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import create_tables, delete_tables, new_session
from db import User
from data_models import UserModel, WatchesModel


async def main():
    print(new_session)
    await create_tables()
    async with new_session() as session:
        query = select(User).options(joinedload(User.watch)).order_by(User.id)
        result = await session.execute(query)
        users = result.scalars().all()
        datas = [UserModel.model_validate(user) for user in users]
        print(list(datas))


if __name__ == "__main__":
    asyncio.run(main())
