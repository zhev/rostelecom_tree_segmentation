import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import hbold
import aiohttp

# Вставьте ваш токен
API_TOKEN = 'YOUR_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Кнопки для отправки ссылок на документацию
markup = types.InlineKeyboardMarkup()
markup.add(
    types.InlineKeyboardButton(text="FastAPI", url="https://fastapi.tiangolo.com/"),
    types.InlineKeyboardButton(text="AIOgram", url="https://docs.aiogram.dev/en/latest/"),
    types.InlineKeyboardButton(text="TensorFlow", url="https://www.tensorflow.org/"),
)

# API-адрес
API_URL = "http://your_fastapi_server_address/image_processing"


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я - бот для обработки изображений. Отправь мне изображение для начала работы.")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = ("Просто отправьте мне изображение, и я обработаю его.\n\n"
                 "Также вы можете воспользоваться следующими командами:\n"
                 "/start - Запуск бота\n"
                 "/help - Порядок использования\n"
                 "/info - Краткая информация об используемых технологиях\n"
                 "/user_id - Информация о пользователе")
    await message.reply(help_text)


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    info_text = "Я использую следующие технологии:\n\n- FastAPI\n- AIOgram\n- TensorFlow"
    await message.reply(info_text, reply_markup=markup)


@dp.message_handler(commands=['user_id'])
async def send_user_id(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    await message.reply(f"ID пользователя: {user_id}\nИмя пользователя: {user_name}")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    await message.reply("Обработка изображения...")

    photo = message.photo[-1]
    photo_file = await bot.get_file(photo.file_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(photo_file.file_path) as resp:
            image_url = str(resp.url)

    async with aiohttp.ClientSession() as session:
        payload = {
            "client": "bot",
            "chat_id": message.chat.id,
            "image_url": image_url
        }
      async with session.post(API_URL, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                processed_image_url = data["image_url"]
                filename = data["filename"]
                resolution = data["resolution"]
                size = data["size"]

                text = (f"Обработанное изображение:\n\n"
                        f"Имя файла: {hbold(filename)}\n"
                        f"Разрешение: {hbold(resolution)}\n"
                        f"Размер: {hbold(size)}")

                await bot.send_photo(chat_id=message.chat.id, photo=processed_image_url, caption=text, parse_mode=ParseMode.MARKDOWN)
            else:
                error_message = await resp.text()
                await message.reply(f"Ошибка обработки изображения: {error_message}")

if name == 'main':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
