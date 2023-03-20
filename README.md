# Telegram ChatGPT3 bot
Персональный чатбот для Telegram использующий OpenAI GPT-3 datasets.

# Setup
1. Установите все пакеты
```
pip install -r install.txt
```
2. Получите <a target="_blank"  href="https://platform.openai.com/account/api-keys">OpenAI API ключ в разделе с вашим аккаунтом </a>
3. Добавьте полученый ключ

```
openai.api_key = (" Ваш API ключ")
```
4. Создайте Telegram бот <a target="_blank" href="https://t.me/BotFather">@BotFather</a>
5. Вставьте полученный токен bot.py with your bot token, OpenAI Token and model name.
```
bot = Bot(token="Ваш токен")
```
6. Вперед!
