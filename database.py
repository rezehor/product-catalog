from beanie import init_beanie
from pymongo import AsyncMongoClient
from models.filters import Filter
from models.products import Product
from settings import settings


async def init_db() -> None:
    """
        Initialize MongoDB connection and Beanie ODM.

        - Creates an asynchronous MongoDB client using the URI from settings.
        - Initializes Beanie with all registered document models (e.g., Product, Filter).
        - Must be called at application startup before any database operations.

        Raises:
            beanie.exceptions.CollectionWasNotInitialized:
                If the document models are not properly initialized.
        """
    client = AsyncMongoClient(settings.MONGODB_URI)

    await init_beanie(
        database=client.get_database(settings.MONGODB_DB_NAME),
        document_models=[Product, Filter],
    )
