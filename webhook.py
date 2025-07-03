import os
from flask import Flask, request
from telegram import Bot

app = Flask(__name__)

# Загружаем из Railway переменные
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPERATOR_CHAT_ID = int(os.getenv("OPERATOR_CHAT_ID"))

bot = Bot(token=BOT_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data.get("event") == "payment.succeeded":
        payment_info = data.get("object", {})
        metadata = payment_info.get("metadata", {})
        user_id = metadata.get("tg_user_id")
        amount = payment_info.get("amount", {}).get("value")

        if user_id and amount:
            try:
                user_id = int(user_id)
                bot.send_message(chat_id=user_id, text=f"✅ Оплата прошла успешно! Сумма: {amount}₽")
                bot.send_message(chat_id=OPERATOR_CHAT_ID, text=f"✅ Онлайн-заказ оплачен на {amount}₽")
            except Exception as e:
                print(f"[Webhook Error] {e}")

    return '', 200
