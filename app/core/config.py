from pydantic_settings import BaseSettings
import os
class Settings(BaseSettings):
    DATABASE_URL: str
    BEDROCK_MODEL_ID: str
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        case_sensitive = True
        extra = "ignore"
settings = Settings()