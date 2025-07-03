import os
from flask import Flask, request
from yookassa import WebhookNotification
from telegram import Bot

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPERATOR_CHAT_ID = int(os.getenv("OPERATOR_CHAT_ID"))

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    notification = WebhookNotification(request.json)

    if notification.event == 'payment.succeeded':
        metadata = notification.object.metadata
        user_id = int(metadata.get("tg_user_id"))
        amount = notification.object.amount.value

        # Уведомляем пользователя
        bot.send_message(chat_id=user_id, text=f"✅ Оплата прошла успешно! Сумма: {amount}₽")

        # Уведомляем оператора
        bot.send_message(chat_id=OPERATOR_CHAT_ID, text=f"✅ Онлайн-заказ оплачен на {amount}₽")

    return '', 200
