from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from moneynote.routers import book_templates, currencies, system, users
from moneynote.services.data_loader_service import DataLoaderService, DataFileError
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    data_loader = DataLoaderService()
    try:
        data_loader.load_all_data(settings)
        app.state.currencies = data_loader.currencies
        app.state.book_templates = data_loader.book_templates
        logging.info("Successfully loaded static data.")
    except DataFileError as e:
        logging.critical("Failed to load static data on startup. Application will not start. Error: %s", e)
        raise
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(system.router, tags=['System'])
app.include_router(currencies.router)
app.include_router(book_templates.router, prefix="/book-templates", tags=["book-templates"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}