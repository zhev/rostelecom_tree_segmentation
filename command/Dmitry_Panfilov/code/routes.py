from fastapi import APIRouter, HTTPException
from schemas import *
from config import TELEGRAM_USERS
from utils import imager

mrt = APIRouter()

@mrt.post('/image_processing', tags=["test"])
async def image_processing(client_message: ClientMessage) -> RespSchema:
    if client_message.client is None:
        client_message.client = 'web'
    
    client = client_message.client.lower()
    img_url = client_message.image_url
    
    if client == 'bot':
        if client_message.chat_id is None:
            raise HTTPException(status_code=400, 
                                detail='Нет CHAT_ID!')
            
        cid = client_message.chat_id
        # Restrict access to specific users (optional)
        if cid not in TELEGRAM_USERS:
            raise HTTPException(status_code=403, 
                                detail='Доступ ЗАПРЕЩЕН!')
        ans = imager(img_url)
    elif client == 'web':
        ans = imager(img_url)
    elif client == 'android':
        ans = imager(img_url)
    else:
        raise HTTPException(status_code=410, 
                            detail='Неизвестный Тип Данных!')

    if ans.code != 200:
        raise HTTPException(status_code=ans.code, 
                    detail=f'Ошибка: {ans.message}')
    
    return RespSchema(**ans)
