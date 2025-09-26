from schemas.filters import Operator, LogicalOperator, FilterResponseSchema


def build_query(filter_data: FilterResponseSchema):
    """
    Convert a FilterResponseSchema into a MongoDB query dictionary.

    Builds a query by translating each condition's operator into the
    corresponding MongoDB filter. Combines all conditions using the
    filter's logical operator (AND / OR).

    Parameters:
        filter_data (FilterResponseSchema): Filter containing conditions and logical operator.

    Returns:
        dict: MongoDB-compatible query dictionary.
    """

    filter_conditions = []

    for cond in filter_data.conditions:
        field, op, value = cond.field, cond.operator, cond.value

        if op == Operator.EQ:
            filter_conditions.append({field: value})
        elif op == Operator.NEQ:
            filter_conditions.append({field: {"$ne": value}})
        elif op == Operator.GT:
            filter_conditions.append({field: {"$gt": value}})
        elif op == Operator.GTE:
            filter_conditions.append({field: {"$gte": value}})
        elif op == Operator.LT:
            filter_conditions.append({field: {"$lt": value}})
        elif op == Operator.LTE:
            filter_conditions.append({field: {"$lte": value}})
        elif op == Operator.INCLUDE:
            filter_conditions.append(
                {field: {"$in": value if isinstance(value, list) else [value]}}
            )
        elif op == Operator.REGEX:
            filter_conditions.append({field: {"$regex": value, "$options": "i"}})

    return (
        {"$and": filter_conditions}
        if filter_data.logical_operator == LogicalOperator.AND
        else {"$or": filter_conditions}
    )
