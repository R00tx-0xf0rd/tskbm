from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator


class BaseClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WatchesModel(BaseClass):
    id: int
    ser_num: str


class BaseUserModel(BaseClass):
    id: int
    tabnum: int
    column: int
    lname: str
    fname: str
    pname: str
    last_checkout: datetime

    @field_serializer("last_checkout")
    def serialize_dt(self, dt: datetime, _info):
        return datetime.strftime(dt, "%d.%m.%Y %H:%M")


class UserModel(BaseUserModel):
    watch: WatchesModel


class AllUsersModel(BaseClass):
    users: list[BaseUserModel]
