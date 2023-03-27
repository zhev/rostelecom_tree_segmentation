import json

# Load environment variables from env.json
with open("env.json") as f:
    env_data = json.load(f)

TELEGRAM_TOKEN = env_data["TELEGRAM_TOKEN"]
TELEGRAM_USERS = env_data["TELEGRAM_USERS"]
