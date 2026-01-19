from fastapi import FastAPI
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

app = FastAPI(
    title = settings.app_name,
    description = settings.description_name,
    version = "1.0.0",
    debug = settings.debug,
    docs_url = "/docs",
    redoc_url = "/redoc",
    openapi_url = "/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_root():
    return {"status": "ok"}