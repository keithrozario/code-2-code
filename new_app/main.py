import logging
from contextlib import asynccontextmanager

from config import settings
from fastapi import FastAPI
from moneynote.routers import book_templates, currencies, system
from moneynote.services.data_loader_service import DataLoaderService, DataFileError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    data_loader = DataLoaderService()
    try:
        data_loader.load_all_data(settings)
        app.state.currencies = data_loader.currencies
        app.state.book_templates = data_loader.book_templates
        logging.info("Static data loaded successfully.")
    except DataFileError as e:
        logging.critical(
            "Failed to load static data on startup. Application will not start. Error: %s",
            e,
        )
        raise
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(system.router, prefix="/api/v1", tags=["System"])
app.include_router(currencies.router, prefix="/api/v1", tags=["Currencies"])
app.include_router(book_templates.router, prefix="/api/v1", tags=["Book Templates"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
