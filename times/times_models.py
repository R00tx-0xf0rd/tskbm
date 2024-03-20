from datetime import datetime

from pydantic import BaseModel, ConfigDict

from data_models import BaseClass


class Period(BaseClass):
    checkout_time: datetime


class UserTimes(BaseClass):
    tabnum: int
    lname: str
    fname: str
    pname: str
    column: int
    times: list["Period"]
