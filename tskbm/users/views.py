from fastapi import APIRouter


from . import crud
from .models import CreateUser

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user)
