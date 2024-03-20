import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import asyncio
from sqlalchemy import select

from db import create_tables, delete_tables, new_session
from db import User
from data_models import UserModel, WatchesModel
from db.database import db_helper
from times.crud import get_times_via_tabnum

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data1 = {1: "one",
             2: "two",
             3: "three",
             "page": "<h1>Hello</h1>"
             }
    data = [data1, [1, 3, 5], "asd", "dsf", 334, "32323"]
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


# @app.get("/page/{page_name}", response_class=HTMLResponse)
# async def show_page(request: Request, page_name: str):
#     return templates.TemplateResponse("page.html", {"request": request, "data": data})


# async def main():
#     # print(new_session)
#     # session = session_dependency()
#     # user = await get_user_by_tabnum(55909)
#     # await create_tables()
#     async with new_session() as session:
#         # query = select(User).options(joinedload(User.watch)).order_by(User.id)
#         query = select(User).order_by(User.id)
#         result = await session.execute(query)
#         users = result.scalars().all()
#         datas = [UserModel.model_validate(user) for user in users]
#         for data in datas:
#             print(data.model_dump_json())


# async def tmp():
#     async with new_session() as session:
#         # new_session = db_helper.session_dependency()
#         # user = await get_user_by_tabnum(session=session, tabnum=55909)
#         # watch = await add_watch(session=session, serial_number="another serial 123")
#         # user = User(
#         #     tabnum=87477,
#         #     lname="Серов",
#         #     fname="Александр",
#         #     pname="Александрович",
#         #     column=9,
#         # )
#         # mash = await create_user(session, user)
#         t = await get_times_via_tabnum(session, 36744)
#         # u = await attach_watches_to_user_by_tabnum(session, 36744, "another serial 123")
#         print(f"{t=}")


if __name__ == "__main__":
    # asyncio.run(tmp())
    uvicorn.run("main:app", port=8080, reload=True)
