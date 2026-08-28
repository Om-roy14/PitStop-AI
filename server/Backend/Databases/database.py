import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================================
# DATABASE CONNECTION URL
# ==========================================
# Check if a cloud DATABASE_URL is provided (e.g., by Railway/Aiven)
DATABASE_URL = os.getenv("DATABASE_URL")

# Otherwise, fall back to building it from local config
if not DATABASE_URL:
    from Backend.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    encoded_password = quote_plus(DB_PASSWORD)
    DATABASE_URL = (
        f"mysql+pymysql://"
        f"{DB_USER}:{encoded_password}"
        f"@{DB_HOST}/{DB_NAME}"
    )

# ==========================================
# ENGINE & SESSION SETUP
# ==========================================
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"fake_flag_to_enable_ssl": True}} # Allows Aiven MySQL connections
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ==========================================
# FASTAPI DEPENDENCY
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()