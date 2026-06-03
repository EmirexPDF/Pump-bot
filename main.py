import os
from flask import Flask, request
import telebot

# Fetch the token from environment variables (configured later on Render)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Dictionary to simulate your product database
PRODUCTS = {
    "trpep-alpha": "🌟 Trpep Alpha: Our premium package offering full access, 24/7 support, and advanced features.",
    "trpep-beta": "⚡ Trpep Beta: Great for starters! Includes standard features and core community access.",
}

# 1. Telegram Command Handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Welcome to the **Trpep Product Bot**! 🚀\n\n"
        "Use `/product [name]` to look up a specific item.\n"
        "Example: `/product trpep-alpha`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['product'])
def lookup_product(message):
    try:
        # Extract product name from command (e.g., /product trpep-alpha -> trpep-alpha)
        product_name = message.text.split(' ', 1)[1].strip().lower()
        
        if product_name in PRODUCTS:
            response = PRODUCTS[product_name]
        else:
            response = f"❌ Product '{product_name}' not found. Try searching for 'trpep-alpha' or 'trpep-beta'."
            
    except IndexError:
        response = "Please specify a product name. Example: `/product trpep-alpha`"

    bot.reply_to(message, response)

# 2. Webhook Infrastructure for Render
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # Replace 'your-render-url.onrender.com' dynamically if needed, 
    # but Render provides an external URL we will link up later.
    return "Trpep Bot is running live!", 200

if __name__ == "__main__":
    # Flask runs on port 5000 by default or uses Render's assigned port
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
