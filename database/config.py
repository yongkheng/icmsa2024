from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str
    base_url: str
    db_url: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: str
    mail_server: str
    mail_from_name: str
    editor_email: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name} {settings.mail_username}")
    return settings
