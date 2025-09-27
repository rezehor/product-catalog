import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient
from models.filters import Filter
from models.products import Product
from routes.products import router as products_router
from routes.filters import router as filters_router
from routes.search import router as search_router


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
    app.include_router(search_router, prefix="/search")

    mongo_client = AsyncMongoMockClient()
    db = mongo_client.test_db
    await init_beanie(database=db, document_models=[Product, Filter])

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture()
def filter_one_template():
    data = {
        "name": "Filter1",
        "logical_operator": "OR",
        "conditions": [
            {
                "logical_operator": "AND",
                "conditions": [
                    {"field": "test1", "operator": ">", "value": 100},
                    {"field": "test2", "operator": ">=", "value": 10},
                ],
            },
            {
                "logical_operator": "AND",
                "conditions": [
                    {"field": "test3", "operator": "include", "value": "test_value"},
                    {"field": "test4", "operator": "<=", "value": 20},
                ],
            },
        ],
    }
    return data


@pytest.fixture()
def filter_two_template():
    data = {
        "name": "Filter2",
        "logical_operator": "AND",
        "conditions": [
            {
                "logical_operator": "AND",
                "conditions": [
                    {"field": "test1", "operator": ">", "value": 100},
                    {"field": "test2", "operator": ">=", "value": 10},
                ],
            },
            {
                "logical_operator": "OR",
                "conditions": [
                    {"field": "test3", "operator": "include", "value": "test_value"},
                    {"field": "test4", "operator": "<=", "value": 20},
                ],
            },
        ],
    }
    return data


@pytest.fixture()
def products_template():
    data = [
        {
            "name": "Product1",
            "price": 100,
            "test1": 150,
            "test2": 30,
            "test3": ["test_value"],
            "test4": 10,
        },
        {
            "name": "Product2",
            "price": 50,
            "test1": 300,
            "test2": 100,
            "test3": ["test_value", "value"],
            "test4": 15,
        },
        {
            "name": "Product3",
            "price": 60,
            "test1": 15,
            "test2": 250,
            "test3": ["value"],
            "test4": 300,
        },
    ]
    return data
