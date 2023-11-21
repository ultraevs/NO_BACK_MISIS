from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db, engine
from sqlalchemy import select, insert
from .models import Operations
from pydantic import BaseModel
router = APIRouter(tags=["HISTORY"])


class OperationModel(BaseModel):
    user_id: int
    name: str
    number: str
    datee: str


@router.get('/history')
async def get_history(user_id: int, session: Session = Depends(get_db)):
    query = select(Operations).where(Operations.user_id == user_id)
    excursion = session.execute(query).scalar()
    return excursion


@router.post('/add_operations')
async def add_operation(operation: OperationModel, session: Session = Depends(get_db)):
    operation = dict(operation)
    operation_obj = insert(Operations).values(user_id=operation["user_id"], name=operation["name"],
                                             number=operation["number"], datee=operation["datee"])
    session.execute(operation_obj)
    session.commit()