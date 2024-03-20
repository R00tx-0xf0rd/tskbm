from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class WatchesModel(BaseClass):
    id: int
    ser_num: str


class UserModel(BaseClass):
    id: int
    tabnum: int
    lname: str
    fname: str
    pname: str
    column: int
    last_checkout: datetime
    watch: WatchesModel
