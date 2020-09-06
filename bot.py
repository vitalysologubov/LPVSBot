import logging
import time
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from settings import API_KEY


# Логирование
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    filename="logs.log",
    level=logging.INFO
)

def greet_user(update, contex):
    """Приветствие пользователя"""

    first_name = update['message']['chat']['first_name']
    last_name = update['message']['chat']['last_name']

    update.message.reply_text(f"Привет {first_name} {last_name}! Напиши мне, а я тебе отвечу ;)")

def talk_to_user(update, context):
    """Отправка сообщения пользователю"""

    text = update.message.text
    update.message.reply_text(text)

def main():
    """Основная функция"""

    my_bot = Updater(API_KEY, use_context=True)

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_user))

    logging.info("Запуск бота.")

    my_bot.start_polling()
    my_bot.idle()

if __name__ == "__main__":
    """Вызов main"""

    main()
