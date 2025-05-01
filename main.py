import random
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = '7243292421:AAG108PmUh_22ziyTwqc2fUmNy8xc0lGaAI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Статистика
stats = {}

start_button = KeyboardButton('Старт')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)

def read_questions(file_path):
    questions = []
    current_question = {'question': '', 'answers': [], 'correct': ''}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('<variant>'):
                current_question['answers'].append(line.replace('<variant>', '').strip())
            elif line.startswith('<variantright>'):
                correct_answer = line.replace('<variantright>', '').strip()
                current_question['answers'].append(correct_answer)
                current_question['correct'] = correct_answer
            elif line:
                if current_question['question']:
                    questions.append(current_question)
                current_question = {'question': line, 'answers': [], 'correct': ''}
        if current_question['question']:
            questions.append(current_question)
    return questions

questions = read_questions('filosofy.txt')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    stats[user_id] = {
        'total': 0,
        'correct': 0,
        'incorrect': 0,
        'current_poll_id': None,
        'correct_option_id': None
    }
    await message.reply("Нажмите 'Старт', чтобы начать опрос.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Старт')
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await send_question(chat_id, user_id)

async def send_question(chat_id, user_id):
    question_data = random.choice(questions)
    question = question_data['question']
    correct_answer = question_data['correct']
    all_answers = question_data['answers']
    random.shuffle(all_answers)

    question_poll = types.Poll(
        question=question.replace("<question> ", ''),
        options=all_answers,
        type='quiz',
        correct_option_id=all_answers.index(correct_answer)
    )

    poll_message = await bot.send_poll(chat_id, question_poll.question, question_poll.options, type=question_poll.type, correct_option_id=question_poll.correct_option_id)
    
    stats[user_id]['current_poll_id'] = poll_message.poll.id
    stats[user_id]['correct_option_id'] = question_poll.correct_option_id

@dp.poll_handler()
async def handle_poll(poll: types.Poll):
    for user_id, data in stats.items():
        if data['current_poll_id'] == poll.id:
            correct_option_id = data['correct_option_id']
            user_answer = poll.options[correct_option_id].voter_count
            if user_answer > 0:
                stats[user_id]['correct'] += 1
            else:
                stats[user_id]['incorrect'] += 1

            stats[user_id]['total'] += 1
            
            await bot.send_message(user_id, f"Всего пройдено вопросов: {stats[user_id]['total']}\nПравильно: {stats[user_id]['correct']}\nНеправильно: {stats[user_id]['incorrect']}")

            try:
                chat_id = await bot.get_chat(user_id)
                await send_question(chat_id.id, user_id)
            except:
                print("Error, ...")
                chat_id = await bot.get_chat(user_id)
                await send_question(chat_id.id, user_id)
            break

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
