from pydantic import BaseModel, ConfigDict


class BaseProduct(BaseModel):
    name: str
    description: str
    price: int


class CreateProduct(BaseProduct):
    pass


class Product(BaseProduct):
    model_config = ConfigDict(from_attributes=True)
    id: int
