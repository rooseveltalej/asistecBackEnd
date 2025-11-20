## Puesta en marcha rápida

### 1) Arrancar todo con un solo comando

- Requisitos: Docker (para Postgres) y Python 3.10+.
- Ejecuta:

```bash
./scripts/dev.sh
```

El script:
- crea el entorno virtual `.venv` si no existe e instala dependencias;
- levanta Postgres con `docker compose` usando las variables de `.env`;
- inicia Uvicorn en modo recarga en `http://0.0.0.0:8000`.

Variables útiles (en línea o exportadas):
- `HOST` y `PORT` para cambiar el bind del servidor.
- `APP_MODULE` (por defecto `app:app`).
- `USE_DOCKER_DB=false` si quieres saltar Docker y usar SQLite/local.

### 2) Alternativa con Make

```bash
# preparar entorno sin ejecutar el servidor
make setup

# ejecutar con Docker para la DB (usa scripts/dev.sh internamente)
make dev

# ejecutar sin docker (solo SQLite o tu propio DATABASE_URL)
make run

# base de datos en contenedor
make db-up     # levantar Postgres
make db-logs   # ver logs
make db-down   # detener y limpiar contenedores
```

### 3) Variables de entorno

El archivo `.env` ya incluye los valores para Postgres:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_DB=asistec
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Opciones:
- Define `DATABASE_URL` para usar cualquier instancia (ej. cloud/local) sin depender de Docker.
- Si `DATABASE_URL` está vacío y existen las variables de Postgres, se usará esa conexión.
- Si no hay Postgres disponible, el backend cae en SQLite local (`test.db`).

### 4) Pruebas

```bash
make test
```

### Notas

- Usa `docker compose` (o `docker-compose` si tu instalación es antigua).
- El servidor arranca con recarga automática (`--reload`).
- Para entornos CI/CD, puedes reutilizar `make setup` y `make test`.
