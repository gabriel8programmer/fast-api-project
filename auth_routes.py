
from fastapi import APIRouter, Depends, HTTPException

from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRES_MINUTE, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from schemas import UserSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def create_token(user_id: int, duration = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTE)):
    expires_date = datetime.now(timezone.utc) + duration
    dict_info = { 'sub': str(user_id), 'exp': expires_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email==email).first()
    if (not user):
        return False
    if (not bcrypt_context.verify(password, user.password)):
        return False
    return user

@auth_router.get('/')
async def home():
    ''''Rota padrão de autenticação'''
    return { 'message': 'Você acessou a rota padrão de autenticação.', 'authenticated': True}

@auth_router.post('/create_account')
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if (user):
        raise HTTPException(status_code=400, detail='Email do usuário já existe!')
    else:
        encrypt_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypt_password)
        session.add(new_user)
        session.commit()
        return { 'message': f"Usuário criado com sucesso! {user_schema.email}"}

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if (not user):
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou senha inválida!')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration=timedelta(days=7))
        return { 'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer' }

@auth_router.get('/refresh')
async def use_refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return { 'access_token': access_token, 'token_type': 'Bearer' }
