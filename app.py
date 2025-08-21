import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from routes import router as api_router
from controllers.areas_controllers import create_area
import schemas

app = FastAPI()

# Incluir todas las rutas de la API
app.include_router(api_router)

# Middleware CORS (ajustar en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (inseguro en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verificar y crear tablas + datos iniciales
inspector = inspect(engine)
if not inspector.get_table_names():
    print("Creando las tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")

    # Crear una sesión de base de datos
    db: Session = next(get_db())

    # Áreas iniciales con su bandera is_major
    initial_areas = [
        {"area_name": "DEVESA", "is_major": False},
        {"area_name": "Escuela Ciencias Naturales y Exactas San Carlos", "is_major": False},
        {"area_name": "Escuela de Ciencias del Lenguaje San Carlos", "is_major": False},
        {"area_name": "Dirección de Campus Tecnológico Local San Carlos", "is_major": False},
        {"area_name": "Ing. En Computación San Carlos", "is_major": True},
        {"area_name": "Ing. Electrónica San Carlos", "is_major": True},
        {"area_name": "Ing. Producción Industrial San Carlos", "is_major": True},
        {"area_name": "Ing. Agronomía San Carlos", "is_major": True},
        {"area_name": "Administración de Empresas San Carlos", "is_major": True},
        {"area_name": "Gestión del Turismo Rural Sostenible San Carlos", "is_major": True},  
        {"area_name": "Gestión en Sostenibilidad Turística Sostenible San Carlos", "is_major": True},  
    ]

    for area_data in initial_areas:
        try:
            create_area(schemas.AreaBase(**area_data), db)
            print(f"Área creada: {area_data['area_name']}")
        except Exception as e:
            print(f"Área omitida: {area_data['area_name']} ({e})")
else:
    print("Las tablas ya existen, omitiendo creación de base de datos.")

# Ruta raíz para prueba
@app.get("/")
async def root():
    return {"message": "API FUNCIONANDO"}
