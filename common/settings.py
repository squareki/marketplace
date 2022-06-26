
from pydantic import AnyUrl, BaseSettings, Field
from sqlalchemy import desc
from sqlalchemy.engine.url import make_url


class Settings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = (
        "{level} {time:YYYY-MM-DD HH:mm:ss} {name}:{function}-{message} | {extra}"
    )
    environment: str = "local"

    class Config:
        env_file_encoding = "utf8"
        env_file = ".env"
        extra = "ignore"

class DatabaseSettings(BaseSettings):
    user: str =  Field(
        ...,
        description="Username for DB",
    )
    password: str = Field(
        ...,
        description="Password for DB",
    )
    url: AnyUrl = Field(
        ...,
        description="URL (DSN) for DB connection",
    )

    @property
    def full_url_sync(self) -> str:
        """
        URL to connect to DB with
        user and password + sync driver
        """
        url = make_url(self.url)
        url = url.set(
            drivername="postgresql",
            username=self.user,
            password=self.password,
        )
        return str(url)
    
    @property
    def full_url_async(self) -> str:
        """
        URL to connect to DB with
        user and password + async driver
        """
        url = make_url(self.url)
        url = url.set(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
        )
        return str(url)
    
    class Config:
        env_prefix = "postgres_"
        env_file_encoding = "utf8"
        env_file = ".env"
        extra = "ignore"

settings = Settings()
database_settings = DatabaseSettings()