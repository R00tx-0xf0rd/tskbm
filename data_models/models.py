from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WatchesModel(BaseModel):
    ser_num: str
    user: int


class UserModel(BaseModel):
    id: int
    tabnum: int
    lname: str
    fname: str
    pname: str
    column: int
    last_checkout: datetime
    watch: int
    # watch: WatchesModel

    # password: str = Field(min_length=4)
    model_config = ConfigDict(from_attributes=True)
