from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    '''
    Configurações gerais usadas na aplicação
    '''
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:1q2w3e4r@localhost:5432/faculdade' #User = geek, Senha = university, banco = faculdade
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()