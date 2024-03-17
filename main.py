import asyncio
from sqlalchemy import select

from db import create_tables, delete_tables, new_session
from db import Users
from data_models import UserModel


async def main():
    print(new_session)
    await create_tables()
    async with new_session() as session:
        query = select(Users).order_by(Users.id)
        result = await session.execute(query)
        users = result.scalars().all()
        datas = [UserModel.model_validate(user) for user in users]
        print(datas)


if __name__ == "__main__":
    asyncio.run(main())
