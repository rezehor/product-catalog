from typing import List
from beanie import PydanticObjectId
from beanie.odm.operators.find.comparison import In
from fastapi import APIRouter, HTTPException, Query, status
from models.products import Product
from schemas.products import (
    ProductListResponseSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
    ProductListCreateSchema,
)

router = APIRouter()


async def get_product_or_404(product_id: PydanticObjectId) -> Product:
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(
            status_code=404, detail="Product with the given ID was not found."
        )
    return product


@router.get(
    "/",
    response_model=ProductListResponseSchema,
    summary="Retrieve a paginated list of products",
    description=(
        "Returns a paginated list of all products in the system. "
        "Supports page number and page size via query parameters. "
        "If no products are found, returns HTTP 404 Not Found."
    ),
)
async def get_all_products(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=20, description="Number of products per page"),
) -> ProductListResponseSchema:

    skip = (page - 1) * per_page
    total_items = await Product.find_all().count()

    if not total_items:
        raise HTTPException(status_code=404, detail="No products found.")

    products = await Product.find_all().skip(skip).limit(per_page).to_list()

    if not products:
        raise HTTPException(status_code=404, detail="No products found.")

    total_pages = (total_items + per_page - 1) // per_page

    response = ProductListResponseSchema(
        products=[
            ProductResponseSchema(**product.model_dump()) for product in products
        ],
        prev_page=(
            f"/products/?page={page - 1}&per_page={per_page}" if page > 1 else None
        ),
        next_page=(
            f"/products/?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
        total_pages=total_pages,
        total_items=total_items,
    )
    return response


@router.get(
    "/{product_id}/",
    response_model=ProductResponseSchema,
    summary="Retrieve a single product by ID",
    description=(
        "Fetches detailed information about a "
        "single product identified by its ID. "
        "If the product does not exist, returns HTTP 404 Not Found."
    ),
)
async def get_product(product_id: PydanticObjectId) -> ProductResponseSchema:
    product = await get_product_or_404(product_id)
    return ProductResponseSchema(**product.model_dump())


@router.post(
    "/",
    response_model=List[ProductResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description=(
        "Creates a new product in the system. "
        "If a product with the same name already exists, "
        "returns HTTP 409 Conflict."
    ),
)
async def create_product(
    product_data: ProductListCreateSchema,
) -> List[ProductResponseSchema]:
    names = [product.name for product in product_data.products]

    existing = await Product.find(In(Product.name, names)).to_list()
    if existing:
        existing_names = [product.name for product in existing]
        raise HTTPException(
            status_code=409,
            detail=f"Product with the name {existing_names} already exists.",
        )

    product_dicts = [product.model_dump() for product in product_data.products]

    products = [Product(**product_dict) for product_dict in product_dicts]

    await Product.insert_many(products)

    return [ProductResponseSchema(**product.model_dump()) for product in products]


@router.patch(
    "/{product_id}/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update an existing product",
    description=(
        "Updates an existing product. Only fields "
        "provided in the request will be updated. "
        "If no valid fields are supplied, returns HTTP 400 Bad Request."
    ),
)
async def update_product(
    product_id: PydanticObjectId, update_data: ProductUpdateSchema
) -> ProductResponseSchema:
    product = await get_product_or_404(product_id)
    updates = update_data.model_dump(exclude_unset=True)

    safe_updates = {}
    for key, value in updates.items():
        if hasattr(product, key):
            current_value = getattr(product, key)
            if value is None or isinstance(value, type(current_value)):
                safe_updates[key] = value
            else:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Field '{key}' must be of type "
                        f"{type(current_value).__name__}"
                    ),
                )

    if not safe_updates:
        raise HTTPException(status_code=400, detail="No valid fields to update.")

    await product.update({"$set": safe_updates})
    return ProductResponseSchema(**product.model_dump())


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
    description=(
        "Deletes a product identified by its ID from the system. "
        "Returns HTTP 204 No Content if deletion succeeds, "
        "or HTTP 404 Not Found if the product does not exist."
    ),
)
async def delete_product(product_id: PydanticObjectId) -> None:
    product = await get_product_or_404(product_id)

    await product.delete()
