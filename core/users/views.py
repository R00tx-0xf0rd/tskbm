from fastapi import APIRouter, Form, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.crud import get_col, get_user_by_tabnum
from data_models import BaseUserModel
from db import User, db_helper

router = APIRouter(prefix="/users")


@router.get("/{tabnum}")
async def get_user_from_tabnum(
    tabnum: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await get_user_by_tabnum(session, tabnum=tabnum)
    print(user)
    if user:
        return user.model_dump()


@router.post("/")
async def get_users_by_column(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    col: int = Form(...),
) -> list[dict]:
    users = await get_col(session, col=col)
    return users
