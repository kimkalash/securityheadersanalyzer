from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Secrets - must be provided via env or .env
    secret_key: str
    jwt_algorithm: str = "HS256"

    # App config
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "sqlite:///./database.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
