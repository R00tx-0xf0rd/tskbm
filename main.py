from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from db import User
from data_models import UserModel, WatchesModel, BaseUserModel
from db.database import db_helper
from core.times.crud import get_times_via_tabnum, create_checkout_time_for_user
from core.users.crud import create_user
from core.users.crud import get_all_users

# routers
from core.users.views import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router)


@app.get("/", response_model=list[BaseUserModel])
# @app.get("/", response_model=list[BaseUserModel])
async def home(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    models = await get_all_users(session)
    users = [BaseUserModel.model_validate(user).model_dump() for user in models]
    # return users
    return templates.TemplateResponse(
        "page.html", {"request": request, "data": users, "extra": [1, 2, 3]}
    )


@app.get("/forms", response_class=HTMLResponse)
def form_get(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "forms.html",
        context={"request": request, "active_page": "forms", "result": result},
    )


@app.get("/temp", response_class=HTMLResponse)
def temp_proc(request: Request):
    return templates.TemplateResponse(
        "temp.html",
        context={"request": request, "active_page": "forms"},
    )


@app.post("/form1", response_class=HTMLResponse)
async def form_post1(
    request: Request,
    tabnum: int = Form(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    model = await get_times_via_tabnum(session, tabnum)
    return templates.TemplateResponse(
        "forms.html", context={"request": request, "data": model, "extra": [1, 2, 3]}
    )


@app.post("/checkout", response_class=HTMLResponse)
async def make_checkout(
    request: Request,
    checkout_tn: int = Form(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    model = await create_checkout_time_for_user(session, checkout_tn)
    return templates.TemplateResponse(
        "forms.html",
        context={"request": request, "checkout": model, "extra": [1, 2, 3]},
    )


@app.post("/form2", response_class=HTMLResponse)
async def add_user(
    request: Request,
    tabnum: int = Form(...),
    column: int = Form(...),
    lname: str = Form(...),
    fname: str = Form(...),
    pname: str = Form(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
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
