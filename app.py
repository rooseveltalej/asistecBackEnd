import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import inspect
from database import engine, Base
from routes import router as api_router


app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (es inseguro en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verificar si la base de datos ya tiene tablas
inspector = inspect(engine)
if not inspector.get_table_names():
    print("Creando las tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas con éxito!")
else:
    print("Las tablas ya existen, omitiendo creación de base de datos.")


@app.get("/")
async def root():
    return {"message": "API FUNCIONANDO"}