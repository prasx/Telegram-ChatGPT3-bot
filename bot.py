import openai
import logging
import sqlite3
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Инициализация OpenAI API
openai.api_key = (" API ")

# Создание экземпляра бота и диспетчера
bot = Bot(token=" API ")
dp = Dispatcher(bot)

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
logging.error("An ERROR")

# Подключение к базе данных
conn = sqlite3.connect('telegram_bot.db')
cursor = conn.cursor()

# Создание таблицы users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        last_message TEXT
    )
""")
conn.commit()

users = {}
stop_symbols = "###"
model = "text-davinci-003"
temperature_text = 0.8

def get_user(id):
    user = users.get(id, {'id': id, 'last_text': '', 'last_prompt_time': 0})
    users[id] = user
    return user

def process_rq(user_id, rq):
    user = get_user(user_id)
    last_text = user['last_text']
       
    # Eсли время последней подсказки > 600 сек удалить контекст
    if time.time() - user['last_prompt_time'] > 600:
        last_text = ''
        user['last_prompt_time'] = 0
        user['last_text'] = ''

    if rq and len(rq) > 0 and len(rq) < 1000:
        print(f"> ({user_id}) {rq}")

       # Удаляем все что полсе 2000 символов
        prompt = f" {last_text} {rq} -> "[-2000:]
        print( "Отправлено: " + prompt ) 
        completion = openai.Completion.create(
            prompt = f"{prompt}\n\nКатя: ",
            engine=model,
            max_tokens=512,
            stop=[stop_symbols],
            temperature=temperature_text
            )
        ans = completion['choices'][0]['text'].strip()
        if "->" in ans:
            ans = ans.split("->")[0].strip()
        ans = ans
        print(f"<< ({user_id}) {ans}") 
        user['last_text'] = prompt + " " + ans + stop_symbols
        user['last_prompt_time'] = time.time()
        return ans
    else:
        user['last_prompt_time'] = 0
        user['last_text'] = ''
        return "\nУпс, кажется что-то пошло не так, напиши @q_b0unc33"

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user = get_user(message.from_user.id)
    user['last_prompt_time'] = 0
    user['last_text'] = ''
    await bot.send_message(message.chat.id, 
                     f"\n Привет,  {message.from_user.first_name}!"
                     f"\nИстория сообщения: очищена 🦧"
                     f"\nВыбранная языковая модель: {model}"
                     f"\nУроверь температуры: {temperature_text}")

@dp.message_handler()
async def echo_all(message):
    user_id = message.from_user.id
    rq = message.text
    ans = process_rq(user_id, rq)
    await bot.send_message(message.chat.id, ans)
    
    # Сохраняем сообщение в базу данных
    cursor.execute("INSERT INTO users (id, name, last_message) VALUES (?, ?, ?)", (message.from_user.id, message.from_user.username, message.text))
    conn.commit()
    
# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)    
