from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError
from typing import Optional


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB: str
    LAMBDA_URL:str
    REDIS_URL:str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )


def load_settings() -> Settings:
    try:
        settings = Settings()
        return settings
    except ValidationError as e:
        print("Environment variable validation failed!")
        for err in e.errors():
            loc = " -> ".join(str(i) for i in err["loc"])
            msg = err["msg"]
            print(f" - {loc}: {msg}")
        raise SystemExit(
            "Application stopped due to missing or invalid environment variables."
        )


settings = load_settings()
