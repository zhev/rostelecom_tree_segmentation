import json

# Загрузка переменных из файла персональных данных env.json (файл не передается на GitHub)
with open("env.json") as f:
    env_data = json.load(f)

TELEGRAM_TOKEN = env_data["TELEGRAM_TOKEN"]
TELEGRAM_USERS = env_data["TELEGRAM_USERS"]
