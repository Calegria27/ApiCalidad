from fastapi import FastAPI
from routes.user import router
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = [
    "http://190.82.118.130",
    "http://190.82.118.130:5174",
    "http://190.82.118.130:5174/login",
    "http://190.82.118.130:5174/home",
    "http://sistratoscalidad.cindependencia.cl",
    "http://sistratoscalidad.cindependencia.cl/login",
    "http://sistratoscalidad.cindependencia.cl/home",
    "http://sistratoscalidad.cindependencia.cl:5174",
    "http://sistratoscalidad.cindependencia.cl:5174/login",
    "http://sistratoscalidad.cindependencia.cl:5174/home",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)

