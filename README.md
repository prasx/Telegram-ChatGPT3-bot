# Telegram ChatGPT3 bot
Personal chatbot for Telegram with disabled OpenAI GPT-3 datasets.

# Setup
1. Install all packages
```
pip install -r install.txt
```
2. Get <a href="https://platform.openai.com/account/api-keys">OpenAI API key from your account </a>
3. Add you OpenAI key

```
openai.api_key = "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"
```

4. Fill your dataset with your answers in `dataset.txt`
5. Validate your dataset
```
openai tools fine_tunes.prepare_data -f dataset.jsonl -q
```
6. Fine-tune your model and get unique model name
```
openai api fine_tunes.create -t dataset.jsonl -m davinci --suffix "<YOUR_MODEL_NAME>"
```
7. Create Telegram bot using BotFather
8. Update tg_bot.py with your bot token, OpenAI Token and model name.
9. Run!
For english version:
```
python tg_bot_eng.py
```
For russian version:
```
python tg_bot_rus.py
```
