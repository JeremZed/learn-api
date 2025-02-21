from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MONGO_URI: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()