from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/data")
async def get_current_date():
    return {"date": datetime.now().date()}
