from pydantic_settings import BaseSettings, SettingsConfigDict
import os 

def path_env():
    work_dir = os.getcwd()
    print(work_dir)
    if work_dir.endswith('src'):
        return '../.env'
    else:
        return './.env'
    
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=path_env(), extra='ignore')

settings = Settings()