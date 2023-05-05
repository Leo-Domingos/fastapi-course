from fastapi import APIRouter
from api.v1.endpoints import curso

api_router = APIRouter()
api_router.include(curso.router, prefix = '/cursos', tags = ['Cursos'])