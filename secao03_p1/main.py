from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Header, Depends
from fastapi.responses import JSONResponse

from models import Curso

from collections import OrderedDict
from typing import List, Optional, Any, Dict

from time import sleep

def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados...')
        sleep(1)

curso_schema = {
    "title": "Curso",
    "type": "object",
    "properties": {
        "id": {"type": "integer", "nullable": True},
        "titulo": {"type": "string"},
        "aulas": {"type": "integer"},
        "horas": {"type": "integer"}
    },
    "additionalProperties": {"type": "integer"}
}

app = FastAPI(
    title= 'API de cursos da Geek University',
    version = '0.0.1',
    description= 'Uma API para estudo do FastAPI'
    )

cursos = {
    1: {
        'Título': 'Programação para leigos',
        'aulas': 112,
        'horas': 58
    },
    2: {
        'Título': 'Algoritmos',
        'aulas': 87,
        'horas': 67
    }
}

@app.get(
        '/cursos', 
        description = 'Retorna todos cursos ou uma lista vazia', 
        summary = 'Retorna todos os cursos',
        response_description= 'Listagem de Cursos',
        responses = {
    200: {
        "description": "Listagem de Cursos", 
        "content": {
            "application/json": {
                "example": {
                    1: {
                        "id": 1,
                        "titulo": "Introdução à Programação",
                        "aulas": 10,
                        "horas": 20,
                    },
                    2: {
                        "id": 2,
                        "titulo": "Banco de Dados",
                        "aulas": 12,
                        "horas": 24,
                    },
                    3: {
                        "id": 3,
                        "titulo": "Desenvolvimento Web",
                        "aulas": 15,
                        "horas": 30,
                    }
         }}}}}
        )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso_by_id(curso_id: int = Path(title = 'ID do curso', description = 'Deve ser entre 1 e 2', gt = 0, lt = 3),db: Any = Depends(fake_db)): ### Se informar o tipo de dado, ele já interpreta como sendo desse tipo
    try:
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Curso não encontrado.')

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso,db: Any = Depends(fake_db)):
    next_id:int = len(cursos) + 1
    if curso.id not in cursos:
        if curso.id is None:
            curso.id = next_id
        cursos[curso.id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'Já existe o curso com ID {curso.id}')
    
@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso,db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        curso.id = curso_id

        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Não existe um curso com id {curso_id}.')
    
@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int,db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Não existe um curso com id {curso_id}')

@app.get('/calculadora')
async def calcular(a: int = Query(gt = 5), b: int = Query(gt = 10), x_geek: str = Header(default = None), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c
    print(f'X-GEEK: {x_geek}')
    return {"resultado" : soma}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host = '0.0.0.0', port = 8000, reload = True)