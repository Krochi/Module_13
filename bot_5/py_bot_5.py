# Задача "Ещё больше выбора"

# Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать' присылалась Inline-клавиатруа.
# Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
# С текстом 'Рассчитать норму калорий' и callback_data='calories'
# С текстом 'Формулы расчёта' и callback_data='formulas'
# Создайте новую функцию main_menu(message), которая:
# Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
# Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'
# Создайте новую функцию get_formulas(call), которая:
# Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
# Будет присылать сообщение с формулой Миффлина-Сан Жеора.
# Измените функцию set_age и декоратор для неё:
# Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
# Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.
# По итогу получится следующий алгоритм:
# Вводится команда /start
# На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
# В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий' и 'Формулы расчёта'
# По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
# По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний по цепочке.


#Решение:

from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Основная клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_first = KeyboardButton(text="Рассчитать")
button_second = KeyboardButton(text="Информация")
kb.add(button_first, button_second)

# Inline-клавиатура для выбора
inline_kb = InlineKeyboardMarkup(row_width=1)
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(button_calories, button_formulas)


# Состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()



@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text=["Информация"])
async def inform(message: types.Message):
    await message.answer("Информация о боте")


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)


@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_text = "Формула Миффлина-Сан Жеора для мужчин"
    await call.message.answer(formula_text)


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (в сантиметрах):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (в килограммах):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    form = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {form:.2f} ккал/день')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




