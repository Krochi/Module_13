import dp
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "7541933458:AAHNNAV6eMyPqgURIy6KSk077JrJCfehiZc"
bot = Bot(token=api)
dp=Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(text=['proverca'])
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")

@dp.message_handler(commands=['start'])
async def start_message(message):
    print("Привет! Я бот помогающий твоему здоровью.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



