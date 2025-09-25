import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
from models.filters import Filter
from models.products import Product
from routes.products import router as products_router
from routes.filters import router as filters_router


@pytest_asyncio.fixture
async def client():
    """
        Creates and yields an HTTPX AsyncClient for testing FastAPI endpoints.

        This fixture sets up an in-memory MongoDB using mongomock_motor,
        initializes Beanie ODM with Product and Filter models, and includes
        the product and filter routers in the FastAPI app. The client can
        be used in asynchronous tests to perform CRUD operations against
        /products and /filters endpoints.

        Yields:
            AsyncClient: An HTTPX async client connected to the FastAPI app.
        """
    app = FastAPI()

    app.include_router(products_router, prefix="/products")
    app.include_router(filters_router, prefix="/filters")

    mongo_client = AsyncMongoMockClient()
    db = mongo_client.test_db
    await init_beanie(database=db, document_models=[Product, Filter])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
