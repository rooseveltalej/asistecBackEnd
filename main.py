from fastapi import FastAPI
from database import engine, Base
from routes import router as api_router
import models
app = FastAPI()

app.include_router(api_router)


# Crear las tablas en la base de datos
print("Creando las tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("¡Tablas creadas con éxito!")
