import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.utils import executor
import filetype
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_docs(message: types.Message):
    document = message.document
    file_path = await document.download()
    kind = filetype.guess(str(file_path.name))
    result = kind.mime if kind else "Unknown format"
    await message.reply(f"Файл определён как: {result}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
