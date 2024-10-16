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
    DATABASE_URL: str = "postgresql://admin:admin@localhost/easygames_db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ADMIN_USER_EMAIL: str
    ADMIN_USER_PASSWORD: str
    ADMIN_USER_FIRST_NAME: str
    ADMIN_USER_LAST_NAME: str

    BUCKET_URL: str = "https://zdybzhhqrimkhrbljuvs.supabase.co/storage/v1/object/public/GamesBucket"

    class Config:
        env_file = ".env"


settings = Settings()
