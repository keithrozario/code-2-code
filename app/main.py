from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.moneynote.services.data_cache_service import DataCacheService
from app.moneynote.routers import system, currencies, book_templates, users, books, groups

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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(system.router, prefix="/api/v1", tags=["System"])
app.include_router(currencies.router, prefix="/api/v1/currencies", tags=["Currencies"])
app.include_router(book_templates.router, prefix="/api/v1/book-templates", tags=["Book Templates"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(groups.router, prefix="/api/v1/groups", tags=["Groups"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
