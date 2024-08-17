# 
# https://github.com
# https://dashboard.render.com
# https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_RENDER_SERVICE_URL>
import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

# Your bot's token from BotFather
TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot and application
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI-powered bot. Use /help to see available commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Welcome message\n/help - List of commands\n/echo - Echo your message\n/ask - Ask me anything")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_echo = ' '.join(context.args)  # Get the message after the /echo command
    if text_to_echo:
        await update.message.reply_text(text_to_echo)
    else:
        await update.message.reply_text("You didn't provide any text to echo!")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = ' '.join(context.args)  # Get the question after the /ask command
    if user_question:
        response = chat_with_openai(user_question)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("You didn't ask anything!")

def chat_with_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Add handlers to application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("echo", echo))
application.add_handler(CommandHandler("ask", ask))

# Flask route to handle incoming webhooks
@app.route('/', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        application.update_queue.put(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
