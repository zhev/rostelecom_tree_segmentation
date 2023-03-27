from pydantic import BaseModel
from typing import Optional

class ClientMessage(BaseModel):
    chat_id: Optional[int]    # для Телеграм
    image_url: str            # ссылка на путь к изображению
    client: Optional[str]     # откуда пришел запрос

class RespSchema(BaseModel):
    code: int
    message: str
    image: bytes
