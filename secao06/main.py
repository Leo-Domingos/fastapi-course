from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title = 'Curso API - Segurança')

app.include_router(api_router, prefix=settings.API_V1_STR)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port = 8000, reload=True, log_level="info")
    
"""
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjgzOTI5NDU3LCJpYXQiOjE2ODMzMjQ2NTcsInN1YiI6IjYifQ.d4VbeONH5zGkjs6J2BNIgOna-Y0bx-p8OdSS2UgANqs
tipo: bearer
"""