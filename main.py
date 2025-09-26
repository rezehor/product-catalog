from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from routes import products, filters, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(title="Product Catalog", lifespan=lifespan)

api_version_prefix = "/api/v1"

app.include_router(
    products.router, prefix=f"{api_version_prefix}/products", tags=["products"]
)
app.include_router(
    filters.router, prefix=f"{api_version_prefix}/filters", tags=["filters"]
)
app.include_router(
    search.router, prefix=f"{api_version_prefix}/search", tags=["search"]
)