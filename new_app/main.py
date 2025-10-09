from fastapi import FastAPI
from contextlib import asynccontextmanager
from moneynote.services.data_loader import load_currencies, load_book_templates
from moneynote.routers import system, currencies, book_templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_currencies()
    load_book_templates()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(system.router, tags=['System'])
app.include_router(currencies.router)
app.include_router(book_templates.router, prefix="/book-templates", tags=["book-templates"])

@app.get("/")
def read_root():
    return {"Hello": "World"}