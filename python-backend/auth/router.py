import sys
sys.path.append("..")
from fastapi import Depends, APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User
from sqlalchemy import select, insert

router = APIRouter()


@router.post("/register")
async def register_user(username: str = Form(...), password: str = Form(...), session: Session = Depends(get_db)):
    query = insert(User).values(username=username, password=password)
    session.execute(query)
    session.commit()


@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...), session: Session = Depends(get_db)):
    query = select(User).where(User.username == username)
    user = session.execute(query).scalar()
    if not user:
        return {"status": 401, "data": "Нет такого юзера"}
    if password != user.password:
        return {"status": 401, "data": "Неверный пароль"}
    if password == user.password:
        return {"status": 200, "data": "Успешно"}