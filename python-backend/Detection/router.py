import sys
sys.path.append('..')
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from Detection.detecton import detect
from parking import current_model
from sqlalchemy import select, insert
from models import Rent
from database import get_db, engine
from sqlalchemy.orm import Session
import logging
router = APIRouter(tags=["Detection"])
model = current_model("Detection/cars.pt")
plates_model = current_model('Detection/plates.pt')
cymbols_model = current_model('Detection/cymbols.pt')


@router.post('/detect')
async def test(cam_id: int, session: Session = Depends(get_db)):
    query = select(Rent).where(Rent.cam_id == str(cam_id))
    rents = session.execute(query).scalars()
    for i in rents:
        print(i)
    answer = detect(model, plates_model, cymbols_model, cam_id)
    return JSONResponse(content=answer)
