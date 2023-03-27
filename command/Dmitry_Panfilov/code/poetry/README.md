## Использование Poetry

**poetry** - продвинутый менеджер зависимостей Python-проектов

1. Установка poetry: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`
или `pip install poetry`
2. Инициализация проекта с помощью poetry: `poetry init`
3. Добавление зависимостей в проект: `poetry add fastapi pydantic requests tensorflow`
4. Активация виртуального окружения: `poetry shell`
5. Запуск сервера: `poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

---

## Использование CUDA (cuDNN) c Tensorflow

Для установки всех зависимостей и драйвера на **Manjaro Linux** для поддержки **CUDA 12.0 и cuDNN** необходимо выполнить следующие шаги:
1.  Установить драйвер NVIDIA, совместимый с CUDA 12.0: `sudo mhwd -a pci nonfree 0300`
2.  Установить **CUDA Toolkit 12.0**. Для этого необходимо скачать установочный файл с официального сайта NVIDIA и запустить его с правами администратора.
3.  Установить библиотеку **cuDNN** версии, совместимой с CUDA 12.0. Для этого нужно зарегистрироваться на официальном сайте NVIDIA и скачать архив с нужной версией cuDNN.
4.  Выполнить команды:
- `sudo cp cuda/lib64/libcudnn* /usr/local/cuda-12.0/lib64/`
- `sudo cp cuda/include/cudnn.h /usr/local/cuda-12.0/include/`
5. Установить зависимости для проекта с помощью Poetry, указав требуемые версии библиотек:
- `poetry install`

---

## Инструменты документации для API

Функции http://localhost:8000/docs и http://localhost:8000/redoc относятся к инструментам документации для API, предоставляемым FastAPI.

- **[docs] http://localhost:8000/docs** отображает интерактивную документацию Swagger UI, которая позволяет пользователям исследовать и тестировать API напрямую через веб-интерфейс. Swagger UI генерирует документацию на основе спецификации OpenAPI, которая автоматически создается FastAPI.

- **[redoc] http://localhost:8000/redoc**, с другой стороны, отображает интерактивную документацию ReDoc, которая также генерируется на основе спецификации OpenAPI. ReDoc имеет более простой и легкий интерфейс, чем Swagger UI, но предоставляет ту же информацию о том, как использовать API.

![image](https://user-images.githubusercontent.com/99917230/227996622-926cf5c1-583f-46d5-a0f9-757e825b5062.png)
