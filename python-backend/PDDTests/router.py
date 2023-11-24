import sys
import datetime
sys.path.append("..")
from fastapi import APIRouter, Depends, Cookie, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, engine
from sqlalchemy import select, insert
from models import Test, Rating, User
from auth.manager import verify_token

router = APIRouter(tags=["PDD_TESTS"])
router.mount("/static", StaticFiles(directory="static"), name="static")
router.mount("/static/tests", StaticFiles(directory="static/tests"), name="static/tests")


@router.get('/test')
async def pdd_test(access_token: str = Cookie(None), session: Session = Depends(get_db)):
    try:
        data = verify_token(access_token)
    except HTTPException:
        return RedirectResponse('/login', status_code=303)
    today = datetime.datetime.now().day
    query = select(Test).where(Test.day == today)
    test = session.execute(query).scalar()
    test = dict(test)
    if access_token not in test["tokens"]:
        return JSONResponse(status_code=200,
                            content={"test_name": test["data"]["name"], "test_questions": test["data"]["questions"], "correct_answer": test["data"]["correct"]})
    elif access_token in test["tokens"]["data"]:
        return JSONResponse(status_code=204, content={"response": "Сегодня тест уже пройден"})


@router.post('/commit-test')
async def commit_test(access_token: str = Cookie(None), session: Session = Depends(get_db)):
    data = verify_token(access_token)
    query = select(User).where(User.email == data["email"])
    user = session.execute(query).scalar()
    query = select(Rating).where(Rating.email == user.email)
    user_rating = session.execute(query).scalar()
    if not user_rating:
        query = insert(Rating).values(email=user.email, count=1)
        session.execute(query)
        session.commit()
        return JSONResponse(status_code=200, content={"count": 1})
    else:
        new_count = user_rating.count + 1
        user_rating.count = new_count
        session.commit()
        return JSONResponse(status_code=200, content={"count": new_count})