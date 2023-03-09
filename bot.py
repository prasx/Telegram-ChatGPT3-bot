import openai
import telebot
import time
import logging
import os

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

# API доступы
openai.api_key = " API "
bot = telebot.TeleBot(" API ")
stop_symbols = "###"
model = "text-davinci-003" # выбор языковой модели, лучшая на текущий момент text-davinci-003 //  gpt-3.5-turbo // gpt-3.5-turbo-0301 - до июня 2023
users = {}



def _get_user(id):
    user = users.get(id, {'id': id, 'last_text': '', 'last_prompt_time': 0})
    users[id] = user
    return user

def _process_rq(user_id, rq):
    user = _get_user(user_id)
    last_text = user['last_text']
    # Eсли время последней подсказки > 600 сек удалить контекст
    if time.time() - user['last_prompt_time'] > 600:
        last_text = ''
        user['last_prompt_time'] = 0
        user['last_text'] = ''

    if rq and len(rq) > 0 and len(rq) < 1000:
        print(f">>> ({user_id}) {rq}")

       # Удаляем все что полсе 2000 символов
        prompt = f" {last_text} {rq} -> "[-2000:]
        print("Sending:" + prompt)
        completion = openai.Completion.create(
            engine=model, prompt=prompt, max_tokens=1024, stop=[stop_symbols], temperature=0.8)
        eng_ans = completion['choices'][0]['text'].strip()
        if "->" in eng_ans:
            eng_ans = eng_ans.split("->")[0].strip()
        ans = eng_ans
        print(f"<<< ({user_id}) {ans}")
        user['last_text'] = prompt + " " + eng_ans + stop_symbols
        user['last_prompt_time'] = time.time()
        return ans
    else:
        user['last_prompt_time'] = 0
        user['last_text'] = ''
        return "Ошибка!"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = _get_user(message.from_user.id)
    user['last_prompt_time'] = 0
    user['last_text'] = ''
    bot.reply_to(message, f"\nПривет,  {message.from_user.first_name}!"
                 f"\nИстория сообщения: очищена 🦧"
                 f"\nВыбранная языковая модель: {model}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    rq = message.text
    ans = _process_rq(user_id, rq)
    bot.send_message(message.chat.id, ans)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(True)
        except Exception:
            logging.exception('Возникла ошибка.')
            time.sleep(10)
            os.execl(sys.executable, sys.executable, *sys.argv)
