from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse

from core.times import create_checkout_time_for_user, get_times_via_tabnum
from db import db_helper

router = APIRouter(prefix="/times", tags=["times"])
templates = Jinja2Templates(directory="templates")


@router.post("/checkout/", response_class=HTMLResponse)
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


@router.post("/tabnum/", response_class=HTMLResponse)
async def get_times(
    request: Request,
    tabnum: int = Form(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    model = await get_times_via_tabnum(session, tabnum)
    return templates.TemplateResponse(
        "forms.html", context={"request": request, "data": model, "extra": [1, 2, 3]}
    )
