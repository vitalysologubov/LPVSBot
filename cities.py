from random import choice


class Cities:
    """Города"""

    def load_cities(self, user_data):
        """Загрузка городов"""

        if 'last_bot_letter' not in user_data:
            user_data['last_bot_letter'] = ''
        
        if 'cities' not in user_data:
            with open('cities.txt', 'r', encoding='utf-8') as cities:
                user_data['cities'] = cities.read().splitlines()

    def check_last_cities(self, user_data, last_letter):
        """Список городов, которые начинаются на последнюю букву предыдущего города"""
        
        return [name for name in user_data['cities'] if name[0].lower() == last_letter.lower()]

    def check_city(self, user_data, user_city):
        """Проверка города"""

        if user_data.get('cities') == []:
            return 'Игра окончена!'
        else:
            if user_city in user_data['cities']:
                first_user_letter = user_city[0].lower()
                last_user_letter = user_city[-1]

                if user_data['last_bot_letter'] != '' and user_data['last_bot_letter'] != first_user_letter:
                    return f'Название города должно начинаться с буквы "{user_data["last_bot_letter"].upper()}"!'
                else:
                    user_data['cities'].remove(user_city)
                    user_cities = self.check_last_cities(user_data, last_user_letter)

                    if user_cities == []:
                        user_data['last_bot_letter'] = ''
                        return f'Города на букву "{last_user_letter}" закончились! Напишите другой город.'
                    else:
                        bot_city = choice(user_cities)
                        user_data['last_bot_letter'] = bot_city[-1]
                        user_data['cities'].remove(bot_city)

                        bot_cities = self.check_last_cities(user_data, user_data['last_bot_letter'])

                        if bot_cities == []:
                            user_data['last_bot_letter'] = ''
                            return (
                                f'{bot_city}. Города на букву "{last_user_letter}" закончились! Напишите другой город.'
                            )
                        else:
                            return f'{bot_city}, ваш ход.'
            else:
                return 'Такой город не найден или уже был использован!'
