from typing import Optional

from pydantic import BaseSettings, Field


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # This variable will be loaded from the .env file. However, if there is a
    # shell environment variable having the same name, that will take precedence.

    # the class Field is necessary while defining the global variables
    ENV_STATE: Optional[str] = Field(..., env="ENV_STATE")
    HOST: Optional[str] = Field(..., env="HOST")
    DB_NAME: Optional[str] = Field(..., env="DB_NAME")
    DB_USERNAME: Optional[str] = Field(..., env="DB_USERNAME")
    DB_PASSWORD: Optional[str] = Field(..., env="DB_PASSWORD")
    DB_HOST: Optional[str] = Field(..., env="DB_HOST")
    DB_PORT: Optional[str] = Field(..., env="DB_PORT")

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


config = FactoryConfig(GlobalConfig().ENV_STATE)()
