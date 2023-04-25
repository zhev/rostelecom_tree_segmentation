# Запустить сервер:
# 
# uvicorn main:app --reload
#

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
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
    # обработку изображения
    # например, размытие
    image = image.filter(ImageFilter.BLUR)
    return image
    

@app.post("/file/segment-file")
async def segment_file(file: UploadFile = File(...)):
    print('Временная директория: ', tempfile.gettempdir())
    image = Image.open(file.file)
    
    # обработка изображения
    image = process_file(image)
    
    # создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # сохраняем измененную картинку во временный файл
        image.save(tmp, format='JPEG')
        
    # возвращаем временный файл как ответ на запрос
    res = FileResponse(tmp.name, filename="processed_" + file.filename)
    
    # удаляем временный файл после ответа на запрос
#    def remove_file():
#        try:
#            shutil.rmtree(tmp.name)
#        except:
#            pass
#    res.background(remove_file)
    
    return res  
  
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
