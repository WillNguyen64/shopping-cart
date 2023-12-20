import os

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


def get_env_file():
    deploy_env = os.getenv("DEPLOY_ENV", "dev")
    return Path(__file__).parent.parent / "config" / "envs" / f"{deploy_env}.env"


class Settings(BaseSettings):
    log_level: str = "INFO"
    db_url: str
    db_trace: bool
    reservation_url: str

    model_config = SettingsConfigDict(env_file=get_env_file())
