import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define la URL de la base de datos (ajusta según tu configuración)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Para SQLite, cambiar según el motor de BD

# Para usar PostgreSQL descomenta las siguientes líneas y configura las variables de entorno
# POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
# POSTGRES_DB = os.getenv("POSTGRES_DB", "database")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Crea el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crea la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependencia para obtener sesión en las rutas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()