from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base de datos SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./geoweather.db"

# Engine con check_same_thread=False para compatibilidad con FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Inyección de dependencia para obtener la sesión de BD por petición"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()