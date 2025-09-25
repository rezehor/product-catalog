from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query, status
from filter_builder import build_query
from models.filters import Filter
from models.products import Product
from schemas.filters import FilterResponseSchema
from schemas.products import ProductListResponseSchema, ProductResponseSchema

router = APIRouter()


@router.get(
    "/{filter_name}/",
    response_model=ProductListResponseSchema,
    summary="Get filtered products",
    description="Get all products filtered by filter_name",
)
async def get_filtered_products(
        filter_name: str,
        page: int = Query(1, ge=1, description="Page number"),
        per_page: int = Query(
            10, ge=1, le=20, description="Number of products per page"
        )
) -> ProductListResponseSchema:
    filter_ = await Filter.find_one(Filter.name == filter_name)
    if not filter_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filter with the name '{filter_name}' was not found."
        )

    filter_data = FilterResponseSchema.model_validate(filter_)

    query = build_query(filter_data)

    skip = (page - 1) * per_page
    total_items = await Product.find(query).count()

    if not total_items:
        raise HTTPException(status_code=404, detail="No products found.")

    products = await Product.find(query).skip(skip).limit(per_page).to_list()

    if not products:
        raise HTTPException(status_code=404, detail="No products found.")

    total_pages = (total_items + per_page - 1) // per_page

    base_url = f"/search/{quote(filter_name)}"

    response = ProductListResponseSchema(
        products=[
            ProductResponseSchema(**product.model_dump())
            for product in products
        ],
        prev_page=(
            f"{base_url}?page={page - 1}&per_page={per_page}"
            if page > 1 else None
        ),
        next_page=(
            f"{base_url}?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
        total_pages=total_pages,
        total_items=total_items,
    )
    return response
