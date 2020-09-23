import ephem
import logging
import time
from additionals import get_random_numbers, get_emoji
from cities import Cities
from glob import glob
from random import choice
from settings import API_KEY
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


class Bot:
    """LPVSBot"""

    def __init__(self):
        """Конструктор класса"""

        self.cities = Cities()
        logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(message)s', level=logging.INFO)

    def start_bot(self):
        """Запуск бота"""

        my_bot = Updater(API_KEY, use_context=True)

        dp = my_bot.dispatcher
        dp.add_handler(CommandHandler('start', self.greet_user))
        dp.add_handler(CommandHandler('quess', self.quess_number))
        dp.add_handler(CommandHandler('cat', self.send_cat))
        dp.add_handler(CommandHandler('planet', self.check_planet))
        dp.add_handler(CommandHandler('wordcount', self.check_word_count))
        dp.add_handler(CommandHandler('fullmoon', self.check_full_moon))
        dp.add_handler(CommandHandler('cities', self.check_city))
        dp.add_handler(CommandHandler('calc', self.calc_numbers))
        dp.add_handler(MessageHandler(Filters.regex('^(Команда /cat)$'), self.send_cat))
        dp.add_handler(MessageHandler(Filters.location, self.get_coordanites))

        logging.info('Запуск бота.')

        my_bot.start_polling()
        my_bot.idle()

    def keyboard(self):
        """Клавиатура"""

        return ReplyKeyboardMarkup([['Команда /cat', KeyboardButton('Отправить координаты', request_location=True)]])

    def greet_user(self, update, context):
        """Приветствие пользователя"""

        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        context.user_data['emoji'] = get_emoji(context.user_data)

        update.message.reply_text(
            f'Привет {first_name} {last_name}! {context.user_data["emoji"]}\n'
            'Поддерживаемые команды:\n'
            '1. /quess [целое число] - придумай и напиши целое число, если оно будет больше моего - ты выиграл!\n'
            '2. /cat - любишь собак? Тогда тебе не повезло! Эта команда покажет тебе котиков!\n'
            '3. /planet [название планеты] - напиши название планеты и узнай в каком созвездии она сейчас находится:\n'
            '- Mercury\n- Venus\n- Mars\n- Jupiter\n- Saturn\n- Uranus\n- Neptune\n'
            '4. /wordcount [текст] - напиши мне что-нибудь, а я подсчитаю сколько в этом слов!\n'
            '5. /fullmoon [ГГГГ-ММ-ДД] - укажи дату и узнай когда будет следующее полнолуние!\n'
            '6. /cities [название города] - уже прошёл GTA 5 и Call of duty: Black ops 4? Тогда попробуй сыграть в '
            'Города!\n'
            '7. /calc [a+b-c*d/e] - выполняй арифметические операции с несколькими числами!',
            reply_markup=self.keyboard()
        )

    def get_coordanites(self, update, context):
        """Получение координат"""

        coords = update.message.location
        message = f'Твои координаты: долгота {coords["longitude"]} и широта {coords["latitude"]}.'
        update.message.reply_text(message)

    def quess_number(self, update, context):
        """Угадывание числа"""

        if context.args:
            try:
                user_number = context.args[0]
                message = get_random_numbers(user_number)
            except (TypeError, ValueError):
                message = 'Введите целое число!'
        else:
            message = 'Введите число!'

        update.message.reply_text(message)

    def send_cat(self, update, context):
        """Отправка картинки с котиками""" 

        photo_list = glob('images/cat*.jpg')
        photo_name = choice(photo_list)
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open(photo_name, 'rb'))

    def check_planet(self, update, context):
        """Проверка планеты"""

        if len(context.args) == 1:
            planet = context.args[0]
            date = time.strftime('%Y/%m/%d')
 
            data = getattr(ephem, planet, None)

            if data:
                constellation = ephem.constellation(data(date))
                update.message.reply_text(f'Планета {planet} находится в созвездии {constellation[1]}.')
            else:
                update.message.reply_text(f'Нет такой планеты в списке.')

    def check_word_count(self, update, context):
        """Проверка количества слов"""

        if len(context.args) != []:
            update.message.reply_text(f'В вашем сообщении {len(context.args)} слов(-а).')
        else:
            update.message.reply_text(f'Введите текст.')

    def check_full_moon(self, update, context):
        """Проверка полнолуния"""

        if len(context.args) == 1:
            date = context.args[0]

            try:
                time.strptime(date, '%Y-%m-%d')
            except ValueError:
                update.message.reply_text(f'Дата не соответствует формату "ГГГГ-ММ-ДД"')
            else:
                moon_date = ephem.next_full_moon(date)
                moon_date = moon_date.datetime().strftime('%H:%M %Y-%m-%d')
                update.message.reply_text(f'Следующее полнолуние будет в {moon_date}.')
        else:
            update.message.reply_text(f'Дата не соответствует формату "ГГГГ-ММ-ДД"')

    def check_city(self, update, context):
        """Проверка города"""

        user_city = update.message.text
        user_city = user_city.replace('/cities ', '').strip()

        if user_city != '':
            self.cities.load_cities(context.user_data)
            message = self.cities.check_city(context.user_data, user_city)
            update.message.reply_text(message)

    def calc_numbers(self, update, context):
        """Подсчёт результата арифметических действий"""

        if context.args != []:
            data = ''.join(context.args)

            try:
                result = eval(data)
                update.message.reply_text(result)
            except NameError:
                update.message.reply_text('Одно из чисел указано неккоректно!')
            except SyntaxError:
                update.message.reply_text('Одно из арифметических действий указано неккоректно!')
            except ZeroDivisionError:
                update.message.reply_text('Деление на ноль недопустимо!')
        else:
            update.message.reply_text('Не соответствует формату! Пример: a+b-c*d/e.')


if __name__ == '__main__':
    """Вызов main"""

    bot = Bot()
    bot.start_bot()
