from fastapi import FastAPI
import logging
from app.moneynote.services.data_cache_service import DataCacheService
from app.moneynote.routers import system

app = FastAPI()

app.include_router(system.router, prefix="/api/v1", tags=["System"])

@app.on_event("startup")
async def startup_event():
    try:
        DataCacheService()
        logging.info("Data cache initialized successfully.")
    except Exception as e:
        logging.critical(f"Failed to initialize DataCacheService: {e}")
        raise e

@app.get("/")
def read_root():
    return {"Hello": "World"}
