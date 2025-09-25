from typing import Any, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, field_validator
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
    field: str
    operator: Operator
    value: Any


class FilterCreateSchema(BaseModel):
    name: str
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

    model_config = {"from_attributes": True}
