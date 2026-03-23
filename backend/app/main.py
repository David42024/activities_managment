from fastapi import FastAPI
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth_router, users_router, categories_router, activities_router

app = FastAPI(
    title = settings.app_name,
    description = settings.description_name,
    version = "1.0.0",
    debug = settings.debug,
    docs_url = "/docs",
    redoc_url = "/redoc",
    openapi_url = "/openapi.json"
)

# CORS Configuration
allowed_origins = [
    "https://activities-managment-front.onrender.com",
    "http://localhost:3000",
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(categories_router, prefix="/api/categories", tags=["Categories"])
app.include_router(activities_router, prefix="/api/activities", tags=["Activities"])


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_root():
    return {"status": "ok"}