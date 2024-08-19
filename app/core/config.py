'''
Config module
'''
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''
    Class for db settings
    '''
    DATABASE_URL: str = "sqlite+aiosqlite:///./easygames_db.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ADMIN_USER_EMAIL: str
    ADMIN_USER_PASSWORD: str
    ADMIN_USER_FIRST_NAME: str
    ADMIN_USER_LAST_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
