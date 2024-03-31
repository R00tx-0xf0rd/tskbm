from pandas import DataFrame as pd
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.crud import get_all_users
from data_models import BaseUserModel
from db import db_helper

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/download/")
async def download_file(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    models = await get_all_users(session)
    users = [BaseUserModel.model_validate(user).model_dump() for user in models]
    # return users
    df = pd(
        users, columns=["tabnum", "column", "lname", "fname", "pname", "last_checkout"]
    )
    df.rename(
        columns={
            "tabnum": "Таб. номер",
            "column": "Колонна",
            "lname": "Фамилия",
            "fname": "Имя",
            "pname": "Отчество",
            "last_checkout": "Последняя проверка",
        },
        inplace=True,
    )
    df.to_excel("output_files/data.xlsx", index=False)
    return FileResponse(
        path="output_files/data.xlsx",
        filename="Статистика проверок ТСКБМ.xlsx",
        media_type="multipart/form-data",
    )
