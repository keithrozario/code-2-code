from fastapi import FastAPI

from database import engine
import models
from api import users, accounts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the MoneyNote API"}
