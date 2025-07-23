
from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import User
from jose import jwt, JWTError

def get_session ():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_id = int(dict_info.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso negado, verifique a validade do token.')

    user = session.query(User).filter(User.id==user_id).first()
    if (not user):
        raise HTTPException(status_code=401, detail='Acesso inválido!')
    return user
