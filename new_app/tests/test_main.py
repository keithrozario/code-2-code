from fastapi import FastAPI
from moneynote.routers import users, book_templates, currencies, system

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(book_templates.router, prefix="/book-templates", tags=["book-templates"])
app.include_router(currencies.router, prefix="/currencies", tags=["currencies"])
app.include_router(system.router, tags=["system"])
