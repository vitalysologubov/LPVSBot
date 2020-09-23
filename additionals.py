from emoji import emojize
from random import choice, randint
from settings import USER_EMOJI


def get_random_numbers(user_number):
    """Получение случайного числа"""

    print(f'user_number: {user_number}')

    try:
        user_number = int(user_number)
    except (TypeError, ValueError):
        message = 'Введите целое число'
    else:
        bot_number = randint(user_number-10, user_number+10)

        if user_number > bot_number:
            message = f'Твоё число {user_number}, моё число {bot_number} - ты выиграл!'
        elif user_number < bot_number:
            message = f'Твоё число {user_number}, моё число {bot_number} - я выиграл!'
        else:
            message = f'Твоё число {user_number}, моё число {bot_number} - ничья!'

    return message


def get_emoji(user_data):
    """Получение эмоджи"""

    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)

        return emojize(smile, use_aliases=True)

    return user_data['emoji']
