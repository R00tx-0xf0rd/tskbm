from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel


class CreateUser(BaseModel):
    tabnum: int
    lname: Annotated[str, MinLen(3), MaxLen(20)]
    fname: Annotated[str, MinLen(3), MaxLen(20)]
    pname: Annotated[str, MinLen(3), MaxLen(20)]
    group: int
