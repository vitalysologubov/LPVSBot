import ephem
import logging
import time
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from settings import API_KEY


# Логирование
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    level=logging.INFO
)

def greet_user(update, contex):
    """Приветствие пользователя"""
    
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    update.message.reply_text(
        f"Привет {first_name} {last_name}!\n"
        "Используя команду /planet, напиши название планеты и узнай в каком созвездии она сейчас находится:\n"
        "1. Mercury\n2. Venus\n3. Mars\n4. Jupiter\n5. Saturn\n6. Uranus\n7. Neptune")

def check_planet(update, contex):
    """Проверка планеты"""

    command = update.message.text.split()

    if len(command) == 2:
        planet = command[1]
        date = time.strftime("%Y/%m/%d")

        try:
            data = getattr(ephem, planet)(date)
        except AttributeError:
            update.message.reply_text(f"Нет такой планеты в списке.")
        else:
            constellation = ephem.constellation(data)
            update.message.reply_text(f"Планета {planet} находится в созвездии {constellation[1]}.")

def main():
    """Основная функция"""

    my_bot = Updater(API_KEY, use_context=True)

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", check_planet))
        
    logging.info("Запуск бота.")

    my_bot.start_polling()
    my_bot.idle()

if __name__ == "__main__":
    """Вызов main"""

    main()
