from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from db import User
from data_models import BaseUserModel
from db.database import db_helper
from core.users.crud import create_user
from core.users.crud import get_all_users

# routers
from core.users.views import router as user_router
from core.times.views import router as times_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan,)#

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
# routers
app.include_router(user_router)
app.include_router(times_router)


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
    uvicorn.run("main:app",host="10.123.20.76", port=8080, reload=True)
