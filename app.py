from fastapi import FastAPI
from routes.user import router
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5174",
    "http://192.168.1.16:5174",
    "http://192.168.1.16:5174/",
    "http://localhost:5174/home",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)

