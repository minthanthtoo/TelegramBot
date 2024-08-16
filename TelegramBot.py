import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    
    # Send a response back to the user
    send_message(chat_id, f"You said: {message_text}")
    
    return "OK", 200

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(BASE_URL, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
