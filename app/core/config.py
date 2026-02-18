from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    db_host: str = Field(alias="DB_HOST")
    db_port: str = Field(alias="DB_PORT")
    db_name: str = Field(alias="DB_NAME")
    db_user: str = Field(alias="DB_USER")
    db_password: str = Field(alias="DB_PASSWORD")
    db_pool_name: str = Field(alias="DB_POOL_NAME")
    db_pool_size: str = Field(alias="DB_POOL_SIZE")

settings = Settings()