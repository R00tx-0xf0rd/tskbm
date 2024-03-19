import asyncio
from sqlalchemy import select
# from sqlalchemy.orm import joinedload

from core.crud import get_user_by_tabnum, add_watch, create_user, attach_watches_to_user_by_tabnum, get_id_by_tabnum, \
    create_checkout_time_for_user
from db import create_tables, delete_tables, new_session
from db import User
from data_models import UserModel, WatchesModel
from db.database import db_helper


async def main():
    # print(new_session)
    # session = session_dependency()
    # user = await get_user_by_tabnum(55909)
    # await create_tables()
    async with new_session() as session:
        # query = select(User).options(joinedload(User.watch)).order_by(User.id)
        query = select(User).order_by(User.id)
        result = await session.execute(query)
        users = result.scalars().all()
        datas = [UserModel.model_validate(user) for user in users]
        for data in datas:
            print(data.model_dump_json())


async def tmp():
    async with new_session() as session:
        # new_session = db_helper.session_dependency()
        # user = await get_user_by_tabnum(session=session, tabnum=55909)
        # watch = await add_watch(session=session, serial_number="another serial 123")
        # user = User(tabnum=87477, lname="Серов", fname="Александр", pname="Александрович", column=9)
        # mash = await create_user(session, user)
        id = await get_id_by_tabnum(session, 55909)
        if id:
            mash = await create_checkout_time_for_user(session, id)
        # u = await attach_watches_to_user_by_tabnum(session, 36744, "another serial 123")
        print(f'{mash=}')


if __name__ == "__main__":
    asyncio.run(tmp())
