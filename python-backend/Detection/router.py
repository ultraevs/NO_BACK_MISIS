import sys
sys.path.append('..')
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Detection.detecton import detect
from parking import current_model
router = APIRouter(tags=["Detection"])
model = current_model("Detection/segmentation.pt")


@router.post('/test')
async def test(cam_id: int):
    answer = detect(model, cam_id)
    return JSONResponse(content=answer)
