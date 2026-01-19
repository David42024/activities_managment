from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str

    access_token_expire_minutes: int = 30
    app_name: str = "Activities Management"
    description_name: str = "API para gestión de actividades operativas"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # ← permite que DATABASE_URL en .env → database_url en Python
    )

# Singleton
settings = Settings()