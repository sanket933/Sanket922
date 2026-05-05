from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    environment: str = 'development'
    api_base_url: str = 'http://localhost:8000'
    database_url: str = 'postgresql+psycopg://postgres:postgres@localhost:5432/company_os'
    redis_url: str = 'redis://localhost:6379/0'
    openai_api_key: str | None = None
    openai_model: str = 'gpt-4.1'
    jwt_secret: str = Field(default='change-me', min_length=8)
    webhook_signing_secret: str = Field(default='change-me', min_length=8)
    make_webhook_base_url: str | None = None
    make_webhook_secret: str | None = None

    smtp_host: str = 'smtp.hostinger.com'
    smtp_port: int = 465
    smtp_username: str = 'info@therisewebd.in'
    smtp_password: str | None = None
    smtp_use_ssl: bool = True
    smtp_fallback_port: int = 587
    imap_host: str = 'imap.hostinger.com'
    imap_port: int = 993
    imap_username: str = 'info@therisewebd.in'
    imap_password: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
