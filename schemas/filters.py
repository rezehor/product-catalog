from typing import Any, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, field_validator, Field
from enum import Enum


class Operator(str, Enum):
    EQ = "=="
    NEQ = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    INCLUDE = "include"
    REGEX = "regex"


class LogicalOperator(str, Enum):
    AND = "AND"
    OR = "OR"


class ConditionSchema(BaseModel):
    field: str = Field(min_length=1, max_length=100)
    operator: Operator
    value: Any


class FilterCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    conditions: list[ConditionSchema]
    logical_operator: LogicalOperator = LogicalOperator.AND

    model_config = {"from_attributes": True}

    @field_validator("conditions")
    @classmethod
    def validate_conditions(cls, value):
        if not value:
            raise ValueError("Filter must contain at least one condition")
        return value


class FilterResponseSchema(FilterCreateSchema):
    id: PydanticObjectId

    model_config = {"from_attributes": True}


class FilterUpdateSchema(BaseModel):
    name: Optional[str] = None
    conditions: Optional[list[ConditionSchema]] = None
    logical_operator: Optional[LogicalOperator] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Name must have at least 1 character")
        return value

    model_config = {"from_attributes": True}
