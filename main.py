import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import asyncio
from sqlalchemy import select

from db import create_tables, delete_tables, new_session
from db import User
from data_models import UserModel, WatchesModel, BaseUserModel
from db.database import db_helper
from times.crud import get_times_via_tabnum
from users.crud import create_user, get_all_users, get_user_by_tabnum, create_checkout_time_for_user

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    async with new_session() as session:
        users: list[BaseUserModel] = await get_all_users(session)
        print(users)
    return templates.TemplateResponse(
        "page.html", {"request": request, "data": users, "extra": [1, 2, 3]}
    )


@app.get("/forms", response_class=HTMLResponse)
def form_get(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "forms.html", context={"request": request, "active_page": "forms", "result": result}
    )


@app.get("/{tabnum}")
async def get_user_from_tabnum(tabnum: int):
    async with new_session() as session:
        user = await get_user_by_tabnum(session, tabnum=tabnum)
        print(user)
        return user.model_dump()


@app.post("/form1", response_class=HTMLResponse)
async def form_post1(request: Request, tabnum: int = Form(...)):
    async with new_session() as session:
        model = await get_times_via_tabnum(session, tabnum)
    return templates.TemplateResponse(
        "forms.html", context={"request": request, "data": model, "extra": [1, 2, 3]}
    )


@app.post("/checkout", response_class=HTMLResponse)
async def make_checkout(request: Request, checkout_tn: int = Form(...)):
    async with new_session() as session:
        model = await create_checkout_time_for_user(session, checkout_tn)
    return templates.TemplateResponse(
        "forms.html", context={"request": request, "checkout": model, "extra": [1, 2, 3]}
    )


@app.post("/form2", response_class=HTMLResponse)
async def add_user(
        request: Request,
        tabnum: int = Form(...),
        column: int = Form(...),
        lname: str = Form(...),
        fname: str = Form(...),
        pname: str = Form(...),
):
    async with new_session() as session:
        user = User(
            tabnum=tabnum,
            column=column,
            lname=lname,
            fname=fname,
            pname=pname,
        )
        mash = await create_user(session, user)
    return templates.TemplateResponse(
        "forms.html", context={"request": request, "mash": mash, "extra": [1, 2, 3]}
    )


if __name__ == "__main__":
    # asyncio.run(tmp())
    uvicorn.run("main:app", port=8080, reload=True)
