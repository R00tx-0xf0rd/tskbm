from pydantic import BaseModel, ConfigDict, Field


class UserModel(BaseModel):
    name: str
    password: str = Field(min_length=4)
    # id: int
    model_config = ConfigDict(from_attributes=True)
