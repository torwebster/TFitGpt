from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://tfit:tfit@localhost:5432/tfit")
    app_secret: str = os.getenv("APP_SECRET", "dev-secret")


settings = Settings()
