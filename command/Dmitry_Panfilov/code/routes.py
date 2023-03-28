# определение API-маршрута для обработки изображений, 
# используя FastAPI для запуска сервера на локальном хосте и порту 8000
# уровень логирования установлен на отладочный (debug), чтобы отслеживать ошибки в коде
# автоматическая перезагрузка при изменении кода (reload=True) упрощает разработку и тестирование приложения
from fastapi import APIRouter, HTTPException
from schemas import *
from config import TELEGRAM_USERS
from utils import imager

mrt = APIRouter()

# API-маршрут принимает POST-запросы по адресу "/image_processing" и принимает объект 
# типа ClientMessage, содержащий информацию о клиенте и URL изображения для обработки
# Если тип клиента не указан, он устанавливается на "web", а дальше
# в зависимости от типа клиента, вызывается функция "imager", которая обрабатывает изображение по заданному URL
@mrt.post('/image_processing', tags=["test"])
async def image_processing(client_message: ClientMessage) -> RespSchema:
    if client_message.client is None:
        client_message.client = 'web'
    
    client = client_message.client.lower()
    img_url = client_message.image_url
    
    # если тип клиента - "bot", то проверяется наличие chat_id в запросе и проверяется, 
    # что он принадлежит списку разрешенных TELEGRAM_USERS;
    # если chat_id не указан или не принадлежит списку разрешенных пользователей, 
    # то возвращается ошибка HTTPException с кодом 400 или 403
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
    
    # Если тип клиента - "web" или "android", то функция "imager" просто возвращает 
    # сегментированное изображение без дополнительной проверки
    elif client == 'web':
        ans = imager(img_url)
    elif client == 'android':
        ans = imager(img_url)
    else:
        raise HTTPException(status_code=410, 
                            detail='Неизвестный Тип Данных!')
    # если тип клиента неизвестен, то возвращается ошибка HTTPException с кодом 410
    if ans.code != 200:
        raise HTTPException(status_code=ans.code, 
                    detail=f'Ошибка: {ans.message}')  # возвращается соответствующая ошибка HTTPException
    
    # если обработка изображения прошла успешно, то возвращается объект из RespSchema
    return RespSchema(**ans)
