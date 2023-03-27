# main.py - основной файл для реализации серверного приложения
# с использованием фреймворка FastAPI по созданию API 3 типов клиентов

# Импорт модулей и компонент из библиотеки FastAPI, 
# а также дополнительного модуля mrt из файла routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from routes import mrt

# Создание объекта FastAPI, который отвечает за обработку запросов и маршрутизацию
app = FastAPI(title="Segmentation_API", version="0.1.0", debug=True)

# CORS Middleware (Cross-Origin Resource Sharing) для обеспечения безопасного обмена данными 
# между сервером и клиентами (веб-приложение, android-приложение),
# для разрешения кросс-доменных запросов от любого домена и настройки заголовков безопасности
app.add_middleware(
    CORSMiddleware,          # добавляет поддержку CORS из FastAPI
    allow_origins=["*"],     # список исходов (доменов), которым разрешено обращаться к API
    allow_credentials=True,  # 
    allow_methods=["*"],     # 
    allow_headers=["*"],     # 
)


app.add_middleware(
    GZipMiddleware,
    minimum_size=1000, # сжимать только ответы размером больше 1000 байт
)

@app.get("/", status_code=200, tags=['test', 'auth'])
def hello():
    "Tree Segmentation Project"
    return "Tree Segmentation Project!"


app.include_router(mrt)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

