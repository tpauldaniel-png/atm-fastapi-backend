from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import users, banks, accounts, atms, auth




app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)



app.include_router(users.router)
app.include_router(banks.router)
app.include_router(accounts.router)
app.include_router(atms.router)
app.include_router(auth.router)



