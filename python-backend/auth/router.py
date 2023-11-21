import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from manager import *
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User
from sqlalchemy import select, insert

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
def register_user(username: str, password: str, session: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    # Сохраните пользователя в базе данных
    query = insert(User).values(username=username,password=password, hashed_password=hashed_password)
    session.execute(query)
    session.commit()
    return {"username": username, "hashed_password": hashed_password}


@router.post("/token")
def authenticate_user(username: str, password: str, session: Session = Depends(get_db)):
    query = select(User).where(User.username == username)
    user = session.execute(query).scalar()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.username})
    return {"access_token": jwt_token, "token_type": "bearer"}