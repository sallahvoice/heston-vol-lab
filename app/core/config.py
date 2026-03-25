from pydantic import Field, SectretStr, AnyUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",
        case_sensitive=True
    )

    app_name: str = Field(default="Heston Vol Lab", alias="APP_NAME")
    environment: Literal["dev", "prod", "test"] = Field(alias="ENVIRONMENT")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(alias="LOG_LEVEL")

    db_url: AnyUrl = Field(alias="DB_URL")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, ge=1, le=65535, alias="DB_PORT")
    db_name: str = Field(default="heston", alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: SectretStr = Field(alias="DB_PASSWORD")
    db_pool_name: Optional[str] = Field(default="default", alias="DB_POOL_NAME")
    db_pool_size: int = Field(default=5, ge=1, le=50, alias="DB_POOL_SIZE")

    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, ge=1, le=65535, alias="REDIS_PORT")
    redis_db: int = Field(default=0, ge=1, le=15, alias="REDIS_DB")
    redis_password: Optional[SectretStr] = Field(default=None, alias="REDIS_PASSWORD")

    api_key: Optional[SectretStr] = Field(default=None, alias="API_KEY")
    #check .env 

settings = Settings()