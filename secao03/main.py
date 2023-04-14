from fastapi import FastAPI, HTTPException, status
from models import Curso

app = FastAPI()

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

@app.get('/cursos')
async def get_cursos():
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso_by_id(curso_id: int): ### Se informar o tipo de dado, ele já interpreta como sendo desse tipo
    try:
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Curso não encontrado.')

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id:int = len(cursos) + 1
    if curso.id not in cursos:
        if curso.id is None:
            curso.id = next_id
        cursos[curso.id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = 'Já existe o curso com ID {curso.id}')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host = '0.0.0.0', port = 8000, reload = True)