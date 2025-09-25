from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from models.products import Product
from schemas.products import ProductCreateSchema, ProductListResponseSchema, ProductResponseSchema, ProductUpdateSchema

router = APIRouter()


async def get_product_or_404(product_id: PydanticObjectId) -> Product:
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product with the given ID was not found.")
    return product


@router.get(
    "/",
    response_model=ProductListResponseSchema,
    summary="List products",
    description="Retrieves a paginated list of products.",
)
async def get_all_products(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=20, description="Number of products per page")
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
        products=[ProductResponseSchema(**product.model_dump()) for product in products],
        prev_page=f"/products/?page={page - 1}&per_page={per_page}" if page > 1 else None,
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
    summary="Get a single product by ID",
    description="Retrieves detailed information for a specific product"
)
async def get_product(product_id: PydanticObjectId) -> ProductResponseSchema:
    product = await get_product_or_404(product_id)
    return ProductResponseSchema(**product.model_dump())


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product.",
    description="Allows all users to add a new product to the database.",
)
async def create_product(product_data: ProductCreateSchema) -> ProductResponseSchema:
    existing = await Product.find_one(Product.name == product_data.name)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Product with the name {product_data.name} already exists."
        )

    product_dict = product_data.model_dump()

    product = Product(**product_dict)

    await product.insert()

    return ProductResponseSchema(**product.model_dump())


@router.patch(
    "/{product_id}/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update a single product.",
    description="Allows all users to update a single product to the database.",
)
async def update_product(
    product_id: PydanticObjectId,
    update_data: ProductUpdateSchema
) -> ProductResponseSchema:
    product = await get_product_or_404(product_id)

    updates = update_data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update."
        )

    await product.update({"$set": updates})
    return ProductResponseSchema(**product.model_dump())


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single product.",
    description="Allows all users to delete a single product to the database.",
)
async def delete_product(product_id: PydanticObjectId):
    product = await get_product_or_404(product_id)

    await product.delete()
