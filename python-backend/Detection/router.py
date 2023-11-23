import sys
sys.path.append('..')
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Detection.detecton import detect
from parking import current_model
import logging
router = APIRouter(tags=["Detection"])
model = current_model("Detection/segmentation.pt")
logging.basicConfig(filename='work.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@router.post('/test')
async def test(cam_id: int):
    answer = detect(model, cam_id)
    return JSONResponse(content=answer)
