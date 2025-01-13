import os
import pathlib
from configparser import ConfigParser
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings

SRC_DIR = pathlib.Path(__file__).parent.parent
ENV = os.environ.get("env", "local").lower()

conf_path = os.path.join(SRC_DIR, "settings", f"{ENV}_config.ini")


class DatabaseSettings(BaseModel):
    host: str
    port: int = 5432
    user: str
    password: str
    db: str
    db_pool_size: int = 20
    max_overflow: int = 30

    @property
    def database_conn_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Auth(BaseModel):
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: str


class AppSettings(BaseSettings):
    database: DatabaseSettings
    jwt: Auth
    model_config = {
        "extra": "allow",
    }

    @classmethod
    def load_from_ini(cls, file_path: str):
        config = ConfigParser()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")

        config.read(file_path)
        config_dict = {section: dict(config.items(section)) for section in config.sections()}

        return cls(**config_dict)


@lru_cache
def get_settings():
    app_config = AppSettings.load_from_ini(conf_path)
    return app_config


if __name__ == "__main__":
    settings = get_settings()
    print(settings)
