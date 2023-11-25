import sys
sys.path.append('..')
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Detection.detecton import detect
from parking import current_model
import logging
router = APIRouter(tags=["Detection"])
model = current_model("Detection/cars.pt")


@router.post('/test')
async def test(cam_id: int, is_debug: bool):
    answer = detect(model, cam_id, is_debug)
    return JSONResponse(content=answer)
