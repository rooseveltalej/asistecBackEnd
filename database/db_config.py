import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
load_dotenv()


def build_postgres_url() -> Optional[str]:
    """Return a Postgres URL if the required vars are present."""
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    if not all([user, password, database]):
        return None

    # Use psycopg3 driver (binary wheel avoids pg_config dependency).
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"


# Prefer an explicit DATABASE_URL, then any Postgres env, and finally SQLite.
SQLALCHEMY_DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or build_postgres_url()
    or "sqlite:///./test.db"
)

engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for DB session injection in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
