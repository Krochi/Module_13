import dp
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ""
bot = Bot(token=api)
dp=Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler(text=['Привет'])
async def meet_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


@dp.message_handler()
async def all_message(message):
    print(f"Полученно сообщение: {message.text}")
    await message.answer(message.text)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



