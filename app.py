from fastapi import FastAPI
from routes.user import router
from config.db import conn

app=FastAPI()


app.include_router(router)