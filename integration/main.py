# Запустить сервер:
# 
# uvicorn main:app --reload
#

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from api_tools import router as api_router

from PIL import Image, ImageFilter
import uvicorn
import io
import tempfile

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

  
def process_file(image):
    """ Производит обработку изображения
        например, размытие
    """
    image = image.filter(ImageFilter.BLUR)
    return image


@app.post("/file/segment-file", response_class=HTMLResponse)
async def segment_file(request: Request, file: UploadFile = File(...)):
    """ Загружает файл, обрабатывает его функцией process_file и так же возвращает файл.
    """
    image = Image.open(file.file)

    # обработка изображения
    image = process_file(image)

    # создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        # сохраняем измененную картинку во временный файл
        image.save(tmp, format='JPEG')
        tmp_path = tmp.name

    # возвращаем временный файл как ответ на запрос
    return RedirectResponse(url=f"/processed-image/{tmp_path.split('/')[-1]}")


@app.get("/processed-image/{filename}", response_class=HTMLResponse)
async def show_processed_image(request: Request, filename: str):
    return templates.TemplateResponse("index.html", {"request": request, "processed_image": f"/files/{filename}"})


@app.get("/files/{filename}")
async def get_image_file(filename: str):
    return FileResponse(f"/tmp/{filename}")
  
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
