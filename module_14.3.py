from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import API

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.add(button)
kb.add(button2)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Рассчитать')
button4 = KeyboardButton(text='Информация')
button5 = KeyboardButton(text = 'Купить')
kb1.add(button3)
kb1.add(button4)
kb1.add(button5)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button6 = InlineKeyboardButton(text = 'Product1',callback_data = 'product_buying')
button7 = InlineKeyboardButton(text = 'Product2',callback_data = 'product_buying')
button8 = InlineKeyboardButton(text = 'Product3',callback_data = 'product_buying')
button9 = InlineKeyboardButton(text = 'Product4',callback_data = 'product_buying')
kb2.row(button6, button7, button8, button9)

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb1)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup=kb)

@dp.message_handler(text = 'Информация')
async def info_message(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for number in range(1, 5):
        await message.answer(f'Название: Продукт {number} /Описание: описание {number} / Цена: {number * 100}')
        with open(f'{number}.jpeg', 'rb') as file:
            await message.answer_photo(file)
    await message.answer(f'Выберите продукт для покупки.', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 x вес(кг)) +(6,25 x рост(см)) – (5 x возраст(г) + 5')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = int(10 * weight + 6.25 * growth - 5 * age + 5)

    await message.answer(f"Ваша норма калорий: {calories}")
    await state.finish()

@dp.callback_query_handler(text="product_buying")
async def back(call):
    await call.message.answer("Вы успешно приобрели этот продукт!", reply_markup=kb2)
    await call.answer()

@dp.message_handler()
async def all__messages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)