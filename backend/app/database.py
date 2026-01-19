
from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import sessionmaker, declarative_base

#Engine -> conexion con PostgreSQL
engine = create_engine(
    settings.database_url, 
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine #uso exclusivo de la base de datos
)

Base = declarative_base() #todas mis tablas van a heredar de esta clase

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()