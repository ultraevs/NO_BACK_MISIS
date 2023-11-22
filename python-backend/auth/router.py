import sys
from datetime import timedelta
sys.path.append("..")
from fastapi import Depends, APIRouter, HTTPException, Form, status, Cookie
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, engine
from models import User
from sqlalchemy import select, insert
from passlib.context import CryptContext
from auth.manager import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_token
router = APIRouter(tags=["AUTH"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get('/register')
async def get_login():
    return FileResponse('static/login.html')


@router.post("/register")
def register_user(
    username: str, password: str, name: str, phone: str, session: Session = Depends(get_db)
):
    user = User(username=username, password_hash=pwd_context.hash(password), name=name, phone=phone)
    session.add(user)
    session.commit()
    session.refresh(user)
    token_data = {"sub": user.id, "username": user.username}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    response = RedirectResponse(url='/profile', status_code=303)
    response.set_cookie(key="access_token", value=access_token)
    return response


@router.get('/login')
async def get_login():
    return FileResponse('static/login.html')


@router.post("/login")
async def login_user(username: str = Form(...), password: str = Form(...), session: Session = Depends(get_db)):
    query = select(User).where(User.username == username)
    user = session.execute(query).scalar()
    if not user:
        return {"status": 401, "data": "Нет такого юзера"}
    if not pwd_context.verify(password, user.password_hash):
        return {"status": 401, "data": "Неверный пароль"}
    token_data = {"sub": user.id, "username": user.username}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    response = RedirectResponse(url='/profile', status_code=303)
    response.set_cookie(key="access_token", value=access_token)
    return response


@router.get("/profile")
async def profile(
    access_token: str = Cookie(None)):
    try:
        data = verify_token(access_token)
        return FileResponse('static/profile.html')
    except HTTPException:
        return RedirectResponse('/login', status_code=303)