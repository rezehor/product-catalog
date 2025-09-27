from typing import Any, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, field_validator, Field
from enum import Enum
from schemas.examples.filters import filter_schema_example


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


class ConditionsMixin(BaseModel):
    """
    Base mixin providing conditions validation.
    Ensures that a filter or nested filter always contains at least one condition.
    """

    conditions: list[Any]

    @field_validator("conditions")
    @classmethod
    def validate_conditions(cls, value):
        if not value:
            raise ValueError("Filter must contain at least one condition")
        return value


class ConditionSchema(BaseModel):
    field: str = Field(min_length=1, max_length=100)
    operator: Operator
    value: Any


class FilterNestedCreateSchema(ConditionsMixin):
    conditions: list[ConditionSchema]
    logical_operator: LogicalOperator = LogicalOperator.AND

    model_config = {"from_attributes": True}


class FilterCreateSchema(ConditionsMixin):
    name: str = Field(min_length=1, max_length=100)
    logical_operator: LogicalOperator = LogicalOperator.AND
    conditions: list[FilterNestedCreateSchema]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {"examples": [filter_schema_example]},
    }


class FilterResponseSchema(FilterCreateSchema):
    id: PydanticObjectId

    model_config = {"from_attributes": True}


class FilterUpdateSchema(ConditionsMixin):
    name: Optional[str] = None
    conditions: Optional[list[FilterNestedCreateSchema]] = None
    logical_operator: Optional[LogicalOperator] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Name must have at least 1 character")
        return value

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {"examples": [filter_schema_example]},
    }
