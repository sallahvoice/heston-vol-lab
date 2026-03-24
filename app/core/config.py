from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    app_name: str = Field(default="Heston Vol Lab", alias="APP_NAME")
    environment: str = Field(default="dev", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    db_url : str = Field(alias="DB_URL")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="heston", alias="DB_NAME")
    db_user: str = Field(default="mysql", alias="DB_USER")
    db_password: str = Field(default="mysql", alias="DB_PASSWORD")
    db_pool_name: Optional[str] = Field(default="default", alias="DB_POOL_NAME")
    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")

    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_password: str | None = Fiedl(default=None, alias="REDIS_PASSWORD")

    api_key: str | None = Field(default=None, alias="API_KEY")
    #check .env 

settings = Settings()