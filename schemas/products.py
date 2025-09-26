from typing import List, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, condecimal, field_validator, Field


class ProductCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: condecimal(ge=0, max_digits=10, decimal_places=2)

    model_config = {
        "from_attributes": True,
        "extra": "allow"
    }


class ProductResponseSchema(BaseModel):
    id: PydanticObjectId
    name: str
    price: float

    model_config = {
        "from_attributes": True,
        "extra": "allow"
    }


class ProductListResponseSchema(BaseModel):
    products: List[ProductResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: Optional[int]
    total_items: Optional[int]

    model_config = {"from_attributes": True}


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[condecimal(ge=0, max_digits=10, decimal_places=2)] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Name must have at least 1 character")
        return value

    model_config = {
        "from_attributes": True,
        "extra": "allow"
    }
