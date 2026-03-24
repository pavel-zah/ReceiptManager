from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
while not (BASE_DIR / ".env").exists() and BASE_DIR.parent != BASE_DIR:
    BASE_DIR = BASE_DIR.parent
ENV_FILE = BASE_DIR / ".env"
print(f"Loading .env from: {ENV_FILE}")

class Settings(BaseSettings):
    """
    Конфигурация приложения.
    """

    # APPLICATION
    app_name: str = "LLM Agent API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"  # development | staging | production

    # API
    api_prefix: str = "/api"
    api_v1_prefix: str = "/api/v1"

    # CORS
    cors_origins: list[str] = ["http://localhost:5432", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # LLM (OpenRouter)
    openrouter_api_key: Optional[str] = None

    openrouter_model: Optional[str] = "qwen/qwen3.5-35b-a3b"

    openrouter_base_url: Optional[str] = "https://openrouter.ai/api/v1"

    openrouter_temperature: float = 0.0
    openrouter_max_tokens: int = 4096
    openrouter_timeout: int = 30  # секунды

    # DATABASE API
    database_api_url: Optional[str] = None

    # LOGGING
    log_level: str = "INFO"  # DEBUG | INFO | WARNING | ERROR
    log_format: str = "text"  # json | text

    # TOOLS
    db_query_max_rows: int = 100
    db_query_timeout: int = 30

    # External API tools
    external_api_enabled: bool = True
    external_api_url: Optional[str] = None
    external_api_key: Optional[str] = None

    # Настройки Pydantic
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,  # Читать из .env файла
        env_file_encoding="utf-8",
        case_sensitive=False,  # DATABASE_URL == database_url
        extra="ignore",  # Игнорировать неизвестные переменные
    )


# Singleton pattern для settings
@lru_cache
def get_settings() -> Settings:
    """
    Создаёт и кеширует единственный экземпляр настроек.
    Использует lru_cache, чтобы не парсить .env каждый раз.
    """
    return Settings()


# Удобный экспорт для импорта
settings = get_settings()