from fastapi import APIRouter, Form, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.crud import get_col, get_user_by_tabnum
from data_models import UserModel
from db import db_helper

router = APIRouter(prefix="/users")


@router.get("/{tabnum}/", response_model=UserModel)
async def get_user_from_tabnum(
    tabnum: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await get_user_by_tabnum(session, tabnum=tabnum)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"tabnum {tabnum} not found"
    )


@router.post("/")
async def get_users_by_column(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    col: int = Form(...),
) -> list[dict]:
    users = await get_col(session, col=col)
    return users
