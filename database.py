from beanie import init_beanie
from pymongo import AsyncMongoClient
from models.filters import Filter
from models.products import Product
from settings import settings


async def init_db():
    client = AsyncMongoClient(settings.MONGODB_URI)

    await init_beanie(
        database=client.get_database(settings.MONGODB_DB_NAME),
        document_models=[Product, Filter],
    )
