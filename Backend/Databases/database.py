import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

# Check if a cloud DATABASE_URL is provided (e.g., by Railway/Aiven)
# Otherwise, fall back to building it from Backend/config.py
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    from Backend.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    encoded_password = quote_plus(DB_PASSWORD)
    DATABASE_URL = (
        f"mysql+pymysql://"
        f"{DB_USER}:{encoded_password}"
        f"@{DB_HOST}/{DB_NAME}"
    )

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()