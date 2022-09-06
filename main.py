import datetime as dt


class Record:
    """
    ПРИМИНИМО ДЛЯ ВСЯХ МЕТОДОВ ВО ВСЕХ КЛАССАХ
    Для большего понимания какие параметры должен принимать метод инициализации
    экземпляра класса лучше использовать явную анотацию типов входных данных
    в этом поможет пакет typing. 
    EXAMPLE:
    def __init__(self, amount: float = 0, comment: str = '', date: str = ''):
    """
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # переменные правильно именовать в нижнем регистре
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # инкремент можно сократить до вида x += y
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        """
        Можно воспользоваться методом isocalendar класса datetime для получения номера текущей недели
        и сравнивать его с номером недели в Записи.
        """
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    """
    Такие коментарии лучше не оставлять.
    По требованиям комментарии к функциям должны быть оформлены в виде Docstrings. https://www.python.org/dev/peps/pep-0257/
    И вообще если метод называется понятным смысловым выражением коментарий о том что он делает можно не писать =)
    например get_today_remaining_calories
    """
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # скобки лучше убрать
            return('Хватит есть!')


class CashCalculator(Calculator):
    """
    Тут мы уже обьявили константы
    """
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    
    """
    Соотвественно в этом методе уберем лишние параметры курсов и получим их из констант в теле метода
    """
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        """
        Это не входит в задание и не укладывается в рамки текущей реализации, но
        я бы рекомендовал вынести получение значений cash_remained и currency_type в отдельный метод,
        а также отдельно сделать сеттер и геттер курсов валют.
        Это позволит тебе в будущем не писать цепочки проверок увеличивая количество строк в этом методе.
        например так
        def convert_cash(currency: str, amount: float):
            available_currency_rate = {
                "usd": {
                    "type": "USD",
                    "rate": 60.00
                },
                "eur": {
                    "type": "Euro",
                    "rate": 70.00
                },
                "rub": {
                    "type": "Руб.",
                    "rate": 1.0
                }
            }
            current_currency = available_currency_rate.get(currency)
            return current_currency.get("type"), amount/current_currency.get("rate")
        тогда вызов будет таким
        currency_type, cash_remained = convert_cash(currency, cash_remained)
        
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # тут явно ошибка - мы не проверяем тут на равенство, а присваиваем значение
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            #можно сделать как в строке 133 - более читаемое форматирование
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
