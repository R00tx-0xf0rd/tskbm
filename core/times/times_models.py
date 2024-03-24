from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer

from data_models import BaseClass


class Period(BaseClass):
    checkout_time: datetime

    @field_serializer("checkout_time")
    def serialize_dt(self, dt: datetime, _info):
        return datetime.strftime(dt, "%d.%m.%Y %H:%M")


class UserTimes(BaseClass):
    tabnum: int
    lname: str
    fname: str
    pname: str
    column: int
    times: list["Period"]
