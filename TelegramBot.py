# 
# https://github.com
# https://dashboard.render.com
# https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_RENDER_SERVICE_URL>

import os
from flask import Flask, request
import telegram
from telegram.ext import CommandHandler, Dispatcher
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Your bot's token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

# Initialize the dispatcher to handle commands
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Command Handlers
def start(update, context):
    update.message.reply_text("Hello! I'm your bot. Use /help to see available commands.")

def help_command(update, context):
    update.message.reply_text("/start - Welcome message\n/help - List of commands\n/echo - Echo your message")

def echo(update, context):
    text_to_echo = ' '.join(context.args)  # Get the message after the /echo command
    if text_to_echo:
        update.message.reply_text(text_to_echo)
    else:
        update.message.reply_text("You didn't provide any text to echo!")

def ask(update, context):
    user_question = ' '.join(context.args)  # Get the question after the /ask command
    if user_question:
        response = chat_with_openai(user_question)
        update.message.reply_text(response)
    else:
        update.message.reply_text("You didn't ask anything!")

def chat_with_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or "gpt-4" if you have access
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"# Add handlers to dispatcher
        
# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("echo", echo))
dispatcher.add_handler(CommandHandler("ask", ask))

# Flask route to handle incoming webhooks
@app.route('/', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
