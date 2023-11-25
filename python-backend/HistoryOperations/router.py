import sys
sys.path.append("..")
from fastapi import APIRouter, Depends, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, engine
from sqlalchemy import select, insert
from models import Operations
from pydantic import BaseModel
from auth.manager import verify_token

router = APIRouter(tags=["HISTORY"])
router.mount("/static", StaticFiles(directory="static"), name="static")


class OperationModel(BaseModel):
    user_id: int
    name: str
    number: str
    datee: str


@router.get('/history')
async def get_history(access_token: str = Cookie(None), session: Session = Depends(get_db)):
    data = verify_token(access_token)
    query = select(Operations).where(Operations.user_id == data["sub"])
    excursion = session.execute(query).scalars()
    return [i for i in excursion]


@router.post('/add_operations')
async def add_operation(operation: OperationModel, access_token: str = Cookie(None), session: Session = Depends(get_db)):
    try:
        data = verify_token(access_token)
    except HTTPException:
        return RedirectResponse('/login', status_code=303)
    operation = dict(operation)
    operation_obj = insert(Operations).values(user_id=data["sub"], name=operation["name"],
                                             number=operation["number"], datee=operation["datee"])
    session.execute(operation_obj)
    session.commit()
