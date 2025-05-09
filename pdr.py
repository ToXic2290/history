
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import random
from lightdb import LightDB

db = LightDB('pdr.json')


API_TOKEN = '7243292421:AAG108PmUh_22ziyTwqc2fUmNy8xc0lGaAI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
start_button = KeyboardButton('Старт')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    db.set(f"u_{user_id}", [])
    await message.reply("Нажмите 'Старт', чтобы начать опрос.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Старт')
async def start(message: types.Message):
    user_id = message.from_user.id
    questions = db.get('questions')
    que = random.choice(questions)
    if len(db.get(f'u_{user_id}')) >= 90:
        return await message.reply("Вопросы закончились. Для очистки базы данных напиши /start")
    while que in q:
        que = random.choice(questions)
    db.set(f'u_{user_id}', (db.get(f'u_{user_id}').append(que)))
    await message.reply(que)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
