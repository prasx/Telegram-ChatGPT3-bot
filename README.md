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
openai.api_key = " You API key"
```

4. Fill your dataset with your answers in `dataset.txt`
5. Validate your dataset
```
openai tools fine_tunes.prepare_data -f dataset.jsonl -q
```
6. Fine-tune your model and get unique model name
```
openai api fine_tunes.create -t dataset.jsonl -m davinci --suffix "Model name"
```
7. Create Telegram bot using BotFather
8. Update bot.py with your bot token, OpenAI Token and model name.
9. Run!