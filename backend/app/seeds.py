# app/seeds.py
from app.database import SessionLocal, Base, engine
from app.models import User, Category
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def run_seeds():
    # 1️⃣ Crear todas las tablas que aún no existan
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Limpiar tablas (orden importa por FKs)
        db.query(Category).delete()
        db.query(User).delete()
        
        # Usuario admin
        admin = User(
            username="admin",
            email="admin@sistema.com",
            password=pwd_context.hash("admin123"),
            role="admin"
        )
        db.add(admin)
        
        # Categorías
        categorias = [
            Category(name="Desarrollo", description="Tareas de desarrollo", color="#3498db"),
            Category(name="Diseño", description="Tareas de diseño UI/UX", color="#9b59b6"),
            Category(name="Testing", description="Pruebas y QA", color="#27ae60"),
            Category(name="Documentación", description="Docs técnicos", color="#f39c12"),
        ]
        db.add_all(categorias)
        
        db.commit()
        print("✅ Seeds ejecutados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()