'''
Config module
'''
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import BaseSettings


class Settings(BaseSettings):
    '''
    Class for db settings
    '''
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env" 


settings = Settings()
