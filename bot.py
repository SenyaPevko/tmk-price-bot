import os

from currency_rater import CurrencyRater
from logger import Logger
from parser import Parser
import telebot
from telebot import types
from dotenv import load_dotenv


class Bot:
    def __init__(self):
        self.parser = Parser()
        self.logger = Logger("bot logger")
        self.currency_rater = CurrencyRater()
        load_dotenv()
        self.token = os.getenv("token")
        self.bot = telebot.TeleBot(self.token)
        self.initialize_bot()

    def start(self):
        self.logger.info("Бот запущен")
        self.bot.polling(none_stop=True)

    def get_default_buttons(self):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        usd_button = types.KeyboardButton('Курс доллара🇺🇸')
        cny_button = types.KeyboardButton('Курс юаня🇨🇳')
        iron_button = types.KeyboardButton('Курс чугуна⛏️')
        steel_button = types.KeyboardButton('Курс стали👷')
        home_button = types.KeyboardButton('В начало🏠')
        about_button = types.KeyboardButton('О боте🤖')
        markup.add(about_button, home_button, usd_button, cny_button, iron_button, steel_button)

        return markup

    def get_currency_buttons(self):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        usd_button = types.KeyboardButton('USD')
        cny_button = types.KeyboardButton('CNY')
        rub_button = types.KeyboardButton('РУБ')
        markup.add(usd_button, cny_button, rub_button)

        return markup

    def show_default_buttons(self, message):
        markup = self.get_default_buttons()
        self.bot.reply_to(message, "Отлично", reply_markup=markup)

    def initialize_bot(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            # Adding default bot commands
            markup = self.get_default_buttons()
            self.bot.reply_to(message,
                         "Привет! Я конвертирую валюты специально для кейса от ТМК. А пока я считаю, можешь выпить вечерний кофий. 😉",
                         reply_markup=markup)
            self.logger.info(f"Отправлено приветственное сообщение пользователю {message.chat.first_name}")

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            match message.text:
                case 'Курс доллара🇺🇸':
                    usd_rate = self.currency_rater.get_currency_rate('USD')
                    if usd_rate is not None:
                        self.bot.reply_to(message, f"Курс доллара (USD): {usd_rate}")
                    else:
                        self.bot.reply_to(message, "Не удалось получить курс доллара.")

                case 'Курс юаня🇨🇳':
                    cny_rate = self.currency_rater.get_currency_rate('CNY')
                    if cny_rate is not None:
                        self.bot.reply_to(message, f"Курс юаня (CNY): {cny_rate}")
                    else:
                        self.bot.reply_to(message, "Не удалось получить курс юаня.")

                case 'Курс чугуна⛏️':
                    start_iron_calculator(message)

                case 'Курс стали👷':
                    start_steel_calculator(message)

                case 'В начало🏠':
                    send_welcome(message)
                case 'О боте🤖':
                    self.about(message)
                case _:
                    self.logger.info(f"Сообщение |{message.text}| не обработано, т.к. нет такой команды.")
                    self.bot.reply_to(message,
                                 f'{message.chat.first_name}, я бы хотел с вами поболтать, но все, что я умею - считать деньги. \n\nБип-бип буп-буп...')

        @self.bot.message_handler(commands=['about'])
        def about_command(message):
            about_text = "Этот бот предоставляет информацию о котировках чермета. "
            about_text += "Если у вас есть вопросы или предложения, свяжитесь с нами."
            self.bot.reply_to(message, about_text)

        @self.bot.message_handler(func=lambda message: message.text == 'Курс чугуна⛏️')
        def start_iron_calculator(message):
            self.bot.reply_to(message, "Введите вес чугуна (в метрических тоннах):")
            self.bot.register_next_step_handler(message, self.process_iron_currency)

        @self.bot.message_handler(func=lambda message: message.text == 'Курс чугуна⛏️')
        def start_steel_calculator(message):
            self.bot.reply_to(message, "Введите вес стали (в метрических тоннах):")
            self.bot.register_next_step_handler(message, self.process_steel_currency)

    def about(self, message):
        self.bot.reply_to(message,
                          "Немного обо мне: \n- Я конвертирую валюты для компании ТМК. \n- Я очень люблю свою работу \n- Курс Юаня и Доллара США выдается по отношеию к Рублю\n- Единицы котировок стали и чугуна соответствуют выдаваемым в сообщениях.")

        self.logger.info(f"Пользователь {message.chat.first_name} запросил информацию о боте")

    def process_metal_weight(self, message, metal_search_name, metal_show_name):
        try:
            weight = float(message.text)
            markup = self.get_currency_buttons()
            self.bot.reply_to(message, "Выберите валюту:", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.process_metal_currency,
                                                metal_search_name, metal_show_name, weight)
        except ValueError:
            self.bot.reply_to(message, "Пожалуйста, введите числовое значение для веса.")

    def process_metal_currency(self, message, metal_search_name, metal_show_name, weight):
        if message.text in ['USD', 'CNY', 'РУБ']:
            currency = message.text
            metal_rate = self.parser.get_commodity_prices(metal_search_name)
            if metal_rate is not None:
                price = float(metal_rate.replace(',', '')) * weight
                price = self.convert_num_from_usd(currency, price)
                self.bot.reply_to(message, f"Цена {metal_show_name} ({weight} метрических тонн): {price:.2f} {currency}")
                self.show_default_buttons(message)
            else:
                self.bot.reply_to(message, f"Не удалось получить курс {metal_show_name}.")
                self.show_default_buttons(message)
        else:
            self.bot.reply_to(message, "Пожалуйста, выберите валюту с помощью кнопок.")

    def process_iron_currency(self, message):
        metal_search_name = "Iron Ore"
        metal_show_name = "чугуна"
        self.process_metal_weight(message, metal_search_name, metal_show_name)

    def process_steel_currency(self, message):
        metal_search_name = "Steel"
        metal_show_name = "стали"
        self.process_metal_weight(message, metal_search_name, metal_show_name)

    def convert_num_from_usd(self, currency, price):
        match currency:
            case "РУБ":
                price *= float(self.currency_rater.get_currency_rate('USD'))
            case "CNY":
                price *= float(self.currency_rater.get_currency_rate('USD'))
                price /= float(self.currency_rater.get_currency_rate('CNY'))

        return price
