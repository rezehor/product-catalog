from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Product(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: Indexed(str, unique=True)
    price: float

    class Settings:
        name = "products"

    class Config:
        extra = "allow"
