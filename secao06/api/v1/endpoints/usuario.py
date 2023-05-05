from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaArtigos, UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp
from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

#GET Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

#POST Usuario
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario:UsuarioModel = UsuarioModel(nome = usuario.nome, sobrenome = usuario.sobrenome, email = usuario.email, senha = gerar_hash_senha(usuario.senha), eh_admin = usuario.eh_admin)
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Email já existe')
    return novo_usuario

#GET Usuarios
@router.get('/',response_model=List[UsuarioSchemaBase])
async def get_usuarios(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios = result.scalars().unique().all()

    return usuarios

#GET Usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario:UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

    if usuario:
        return usuario
    else:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)

#PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario:UsuarioSchemaUp,  db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuarioUp:UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuarioUp:
            if usuario.nome:
                usuarioUp.nome = usuario.nome
            if usuario.sobrenome:
                usuarioUp.sobrenome = usuario.sobrenome
            if usuario.email:
                usuarioUp.email = usuario.email
            if usuario.eh_admin:
                usuarioUp.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuarioUp.senha = gerar_hash_senha(usuario.email)
            await session.commit()
            return usuarioUp
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuarioDel:UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuarioDel:
            await session.delete(usuarioDel)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
#POST Login
@router.post('/login')
async def login(form_data:OAuth2PasswordRequestForm = Depends(), db:AsyncSession = Depends(get_session)):
    usuario = await autenticar(email = form_data.username, senha = form_data.password, db = db)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = 'Dados de acesso incorretos')
    else:
        return JSONResponse(content={"access_token":criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
    