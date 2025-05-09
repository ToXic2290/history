
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import random
from lightdb import LightDB

db = LightDB('pdr.json')
q = []

API_TOKEN = '7243292421:AAG108PmUh_22ziyTwqc2fUmNy8xc0lGaAI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    q = []
    await message.reply("Нажмите 'Старт', чтобы начать опрос.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Старт')
async def start(message: types.Message):
    questions = db.get('questions')
    que = random.choice(questions)
    if len(q) >= 90:
        return await message.reply("Вопросы закончились. Для очистки базы данных напиши /start")
    while que in q:
        que = random.choice(questions)
    q.append(que)
    await message.reply(que)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
