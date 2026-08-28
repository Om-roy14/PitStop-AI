import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =========================================
# DATABASE CONFIGURATION (LOCAL FALLBACK)
# =========================================
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")