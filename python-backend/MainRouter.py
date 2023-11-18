from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sys
sys.path.append('..')
from fastapi.responses import FileResponse
from parking import current_model, detection, token_update
router = APIRouter(tags=["MAIN"])

model = current_model("segmentation.pt")


@router.get('/')
async def main():
    return FileResponse('/static/main.html')


@router.post('/test')
async def test(cam_id: int):
    answer = detection.parking_info(model, cam_id)
    return JSONResponse(content=answer)
