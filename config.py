import os

from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables (like application.properties)

DATABASE_URL = os.environ["DATABASE_URL"]  # fails fast if not set

# comma-separated list of frontend URLs allowed to call the API
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
