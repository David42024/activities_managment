# refresh_db.py
# Borra todo, re-crea tablas y ejecuta seeds

from app.database import engine, Base
from app.models import User, Activity, Category, Historical
from app.seeds import run_seeds


def refresh():
    print("🗑️  Eliminando tablas...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️  Creando tablas...")
    Base.metadata.create_all(bind=engine)
    
    print("🌱 Ejecutando seeds...")
    run_seeds()
    
    print("✅ Base de datos refrescada")


if __name__ == "__main__":
    refresh()