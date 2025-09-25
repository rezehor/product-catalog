from typing import Any
from beanie import Document, PydanticObjectId, Indexed
from pydantic import Field
from schemas.filters import LogicalOperator


class Filter(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: Indexed(str, unique=True)
    conditions: list[dict[str, Any]]
    logical_operator: LogicalOperator = LogicalOperator.AND

    class Settings:
        name = "filters"
