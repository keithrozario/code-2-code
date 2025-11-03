from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from app.moneynote.services.data_cache_service import DataCacheService
from app.moneynote.routers import system, currencies, book_templates, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        DataCacheService()
        logging.info("Data cache initialized successfully.")
    except Exception as e:
        logging.critical(f"Failed to initialize DataCacheService: {e}")
        raise e
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(system.router, prefix="/api/v1", tags=["System"])
app.include_router(currencies.router, prefix="/api/v1/currencies", tags=["Currencies"])
app.include_router(book_templates.router, prefix="/api/v1/book-templates", tags=["Book Templates"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
