from decimal import Decimal
from beanie import Document, Indexed, PydanticObjectId
from bson import Decimal128
from pydantic import Field, field_validator


class Product(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: Indexed(str, unique=True)
    price: Decimal

    @field_validator("price", mode="before")
    @classmethod
    def convert_decimal128(cls, value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    class Settings:
        name = "products"

    class Config:
        extra = "allow"
