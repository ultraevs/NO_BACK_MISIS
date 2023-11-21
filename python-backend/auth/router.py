from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/auth/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
