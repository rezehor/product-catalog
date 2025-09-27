from typing import Any
from schemas.filters import Operator, LogicalOperator, FilterCreateSchema


def build_query(filter_data: FilterCreateSchema) -> dict:
    """
    Convert a FilterCreateSchema into a MongoDB query dictionary.

    Each group of conditions is combined with its own
    logical operator (AND/OR),and all groups are joined
    by the filter's top-level logical operator.

    Args:
        filter_data (FilterCreateSchema): The filter definition.

    Returns:
        dict: MongoDB query dictionary compatible with .find().
    """

    def condition_to_query(field: str, operator: Operator, value: Any) -> dict:
        operator_map = {
            Operator.EQ: lambda val: {field: val},
            Operator.NEQ: lambda val: {field: {"$ne": val}},
            Operator.GT: lambda val: {field: {"$gt": val}},
            Operator.GTE: lambda val: {field: {"$gte": val}},
            Operator.LT: lambda val: {field: {"$lt": val}},
            Operator.LTE: lambda val: {field: {"$lte": val}},
            Operator.INCLUDE: lambda val: {
                field: {"$in": val if isinstance(val, list) else [val]}
            },
            Operator.REGEX: lambda val: {
                field: {"$regex": val, "$options": "i"}
            },
        }
        return operator_map[operator](value)

    groups = []
    for group in filter_data.conditions:
        sub_queries = [
            condition_to_query(cond.field, cond.operator, cond.value)
            for cond in group.conditions
        ]
        if group.logical_operator == LogicalOperator.AND:
            groups.append({"$and": sub_queries})
        else:
            groups.append({"$or": sub_queries})

    return {"$and": groups} \
        if filter_data.logical_operator == LogicalOperator.AND \
        else {"$or": groups}
