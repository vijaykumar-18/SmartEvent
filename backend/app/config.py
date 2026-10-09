import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError("Set SECRET_KEY to a random value of at least 32 characters in backend/.env.")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smartevent.db")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
default_allowed_origins = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "http://0.0.0.0:5173,"
    "http://localhost:3000,"
    "http://127.0.0.1:3000"
)
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", default_allowed_origins).split(",")
    if origin.strip()
]
INITIAL_ADMIN_EMAIL = os.getenv("INITIAL_ADMIN_EMAIL", "").strip().lower()