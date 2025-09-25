from typing import List
from fastapi import APIRouter, HTTPException, status
from models.filters import Filter
from schemas.filters import FilterCreateSchema, FilterResponseSchema, FilterUpdateSchema


router = APIRouter()


async def get_filter_or_404(name: str) -> Filter:
    filter_ = await Filter.find_one(Filter.name == name)
    if not filter_:
        raise HTTPException(404, f"Filter with name '{name}' not found")
    return filter_


@router.post("/", response_model=FilterResponseSchema)
async def create_filter(filter_data: FilterCreateSchema) -> FilterResponseSchema:
    existing_filter = await Filter.find_one(Filter.name == filter_data.name)
    if existing_filter:
        raise HTTPException(
            status_code=409,
            detail=f"Filter with the name {filter_data.name} already exists."
        )

    new_filter = Filter(**filter_data.model_dump())
    await new_filter.insert()
    return FilterResponseSchema.model_validate(new_filter)


@router.get(
    "/",
    response_model=List[FilterResponseSchema],
    summary="List filters",
    description="Retrieves all filters.",
)
async def get_all_filters() -> List[FilterResponseSchema]:
    filters = await Filter.find_all().to_list()
    return [FilterResponseSchema.model_validate(f) for f in filters]


@router.get(
    "/{filter_name}/",
    response_model=FilterResponseSchema,
    summary="Get a filter",
    description="Retrieves a filter by name.",
)
async def get_filter(filter_name: str) -> FilterResponseSchema:
    filter_ = await get_filter_or_404(filter_name)
    return FilterResponseSchema.model_validate(filter_)


@router.patch(
    "/{filter_name}/",
    response_model=FilterResponseSchema,
    summary="Update a filter",
    description="Updates a filter.",
)
async def update_filter(filter_name: str, update_data: FilterUpdateSchema):
    filter_ = await get_filter_or_404(filter_name)

    updates = update_data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update."
        )

    await filter_.update({"$set": updates})
    return FilterResponseSchema.model_validate(filter_)


@router.delete(
    "/{filter_name}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single filter.",
    description="Deletes a single filter by name.",
)
async def delete_filter(filter_name: str):
    filter_ = await get_filter_or_404(filter_name)
    await filter_.delete()
